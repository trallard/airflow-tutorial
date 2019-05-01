""" Simple Airflow data pipeline example using Twitter API """
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.email_operator import EmailOperator
from airflow.hooks import sqlite_hook
from airflow.hooks.mysql_hook import MySqlHook
from tweepy import API, Cursor, OAuthHandler
from configparser import ConfigParser
from csv import DictWriter, writer
from collections import Counter
from datetime import datetime, timedelta
import ast
import itertools
import glob
import shutil
import pandas as pd
import os.path
from pathlib import Path

RAW_TWEET_DIR = Path("../data/tweets/").resolve()
CONFIG_FILE = Path("../../config.cfg").resolve()
MAX_TWEEPY_PAGE = 2

# since there do not exist task on their own we need to create the DAG
default_args = {
    "owner": "admin",
    "depends_on_past": False,
    "start_date": datetime.now() - timedelta(days=5),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG("twitter_links", default_args=default_args, schedule_interval="@daily")


def extract_tweet_data(tweepy_obj, query):
    """ Extract relevant and serializable data from a tweepy Tweet object
        params:
            tweepy_obj: Tweepy Tweet Object
            query: str
        returns dict
    """
    return {
        "user_id": tweepy_obj.user.id,
        "user_name": tweepy_obj.user.name,
        "user_screenname": tweepy_obj.user.screen_name,
        "user_url": tweepy_obj.user.url,
        "user_description": tweepy_obj.user.description,
        "user_followers": tweepy_obj.user.followers_count,
        "user_friends": tweepy_obj.user.friends_count,
        "created": tweepy_obj.created_at.isoformat(),
        "text": tweepy_obj.text,
        "hashtags": [ht.get("text") for ht in tweepy_obj.entities.get("hashtags")],
        "mentions": [
            (um.get("id"), um.get("screen_name"))
            for um in tweepy_obj.entities.get("user_mentions")
        ],
        "urls": [url.get("expanded_url") for url in tweepy_obj.entities.get("urls")],
        "tweet_id": tweepy_obj.id,
        "is_quote_status": tweepy_obj.is_quote_status,
        "favorite_count": tweepy_obj.favorite_count,
        "retweet_count": tweepy_obj.retweet_count,
        "reply_status_id": tweepy_obj.in_reply_to_status_id,
        "lang": tweepy_obj.lang,
        "source": tweepy_obj.source,
        "location": tweepy_obj.coordinates,
        "query": query,
    }


def search_twitter(**kwargs):
    """ Search for a query in public tweets"""
    query = kwargs.get("params").get("query")
    config = ConfigParser()
    config.read(CONFIG_FILE)
    auth = OAuthHandler(
        config.get("twitter", "consumer_key"), config.get("twitter", "consumer_secret")
    )
    auth.set_access_token(
        config.get("twitter", "access_token"),
        config.get("twitter", "access_token_secret"),
    )
    api = API(auth)

    all_tweets = []
    page_num = 0
    since_date = datetime.strptime(kwargs.get("ds"), "%Y-%m-%d").date() - timedelta(
        days=1
    )
    query += " since:{} until:{}".format(
        since_date.strftime("%Y-%m-%d"), kwargs.get("ds")
    )
    print(f"searching twitter with: {query}")
    for page in Cursor(
        api.search, q=query, monitor_rate_limit=True, wait_on_rate_limit=True
    ).pages():
        all_tweets.extend([extract_tweet_data(t, query) for t in page])
        page_num += 1
        if page_num > MAX_TWEEPY_PAGE:
            break

    # if it's an empty list, stop here
    if not len(all_tweets):
        return

    filename = "{}/{}_{}.csv".format(
        RAW_TWEET_DIR, query, datetime.now().strftime("%m%d%Y%H%M%S")
    )

    with open(filename, "w") as raw_file:
        raw_wrtr = DictWriter(raw_file, fieldnames=all_tweets[0].keys())
        raw_wrtr.writeheader()
        raw_wrtr.writerows(all_tweets)


def csv_to_sql(directory=RAW_TWEET_DIR, **kwargs):
    """ csv to sql pipeline using pandas
        params:
            directory: str (file path to csv files)
    """
    dbconn = MySqlHook(mysl_conn_id="mysql_default")
    for fname in glob.glob("{}/*.csv".format(directory)):
        if "_read" not in fname:
            try:
                df = pd.read_csv(fname)
                df.to_sql("tweets", dbconn, if_exists="append", index=False)
                shutil.move(fname, fname.replace(".csv", "_read.csv"))
            except pd.io.common.EmptyDataError:
                # probably an io error with another task / open file
                continue


def identify_popular_links(directory=RAW_TWEET_DIR, write_mode="w", **kwargs):
    """ Identify the most popular links from the last day of tweest in the db
        Writes them to latest_links.txt in the RAW_TWEET_DIR
        (or directory kwarg)
    """
    dbconn = MySqlHook(mysl_conn_id="mysql_default")
    query = """select * from tweets where
    created > date('now', '-1 days') and urls is not null
    order by favorite_count"""
    df = pd.read_sql_query(query, conn)
    df.urls = df.urls.map(ast.literal_eval)
    cntr = Counter(itertools.chain.from_iterable(df.urls.values))
    with open("{}/latest_links.txt".format(directory), write_mode) as latest:
        wrtr = writer(latest)
        wrtr.writerow(["url", "count"])
        wrtr.writerows(cntr.most_common(5))


# --------------------------------------
# Tasks
# -------------------------------------
simple_search = PythonOperator(
    task_id="search_twitter",
    provide_context=True,
    python_callable=search_twitter,
    dag=dag,
    params={"query": "#python"},
)


move_tweets_to_sql = PythonOperator(
    task_id="csv_to_sql",
    # extra DAG context
    provide_context=True,
    # call the function
    python_callable=csv_to_sql,
    dag=dag,
)


id_popular = PythonOperator(
    task_id="identify_popular_links",
    provide_context=True,
    python_callable=identify_popular_links,
    dag=dag,
)


email_links = EmailOperator(
    task_id="email_best_links",
    to="trallard@bitsandchips.me",
    subject="Latest popular links",
    html_content="Check out the latest!!",
    files=["{}/latest_links.txt".format(RAW_TWEET_DIR)],
    dag=dag,
)


simple_search.set_downstream(move_tweets_to_sql)
id_popular.set_upstream(move_tweets_to_sql)
email_links.set_upstream(id_popular)
