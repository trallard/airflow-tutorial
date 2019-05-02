# ------------------------------------------------------------------
# This script is used to stream Twitter data into a MySQL my_database
# note that for this you need an approved Twitter develope account
# an app and the keys for said app
# ------------------------------------------------------------------

# Import libraries needed
import sys
import json
import time
from configparser import ConfigParser
from pathlib import Path

import tweepy
from dateutil import parser
from mysql import connector as mysql

# Path to the config file with the keys make sure not to commit this file
CONFIG_FILE = Path.cwd() / "config.cfg"

# Details for our MySql connection
DATABASE = {
    "host": "localhost",
    "user": "airflow",
    "password": "python2019",
    "db": "airflowdb",
}

MAX_TWEEPY_PAGE = 300


# ----------------------------------------------
#  Database related functions
# ----------------------------------------------


def connect_db(my_database):
    """Connect to a given my_database
    
    Args:
        my_database(dict): dictionary with the my_database details
    
    Returns:
        dbconnect: MySql my_database connection object
    """
    try:
        dbconnect = mysql.connect(
            host=my_database.get("host"),
            user=my_database.get("user"),
            password=my_database.get("password"),
            db=my_database.get("db"),
        )
        print("connected")
        return dbconnect
    except mysql.Error as e:
        print(e)


def create_table(my_database, new_table):
    """Create new table in a my_database
    
    Args:
        my_database (dict): details for the db
        new_table (str): name of the table to create
    """

    dbconnect = connect_db(my_database)

    # create a cursor for the queries
    cursor = dbconnect.cursor()
    cursor.execute("USE airflowdb")

    # here we delete the table, it can be kept or else
    cursor.execute(f"DROP TABLE IF EXISTS {new_table}")

    # these matches the Twitter data
    query = (
        f"CREATE TABLE `{new_table}` ("
        "  `id` INT(11) NOT NULL AUTO_INCREMENT,"
        "  `user` varchar(100) NOT NULL ,"
        "  `created_at` timestamp,"
        "  `tweet` varchar(255) NOT NULL,"
        "  `retweet_count` int(11) ,"
        "  `id_str` varchar(100),"
        "  `country` varchar(255),"
        "   `followers` varchar(100),"
        "   `language` varchar(100),"
        "  PRIMARY KEY (`id`))"
    )

    cursor.execute(query)
    dbconnect.close()
    cursor.close()

    return print(f"Created {new_table} table")


def populate_table(
    user,
    created_at,
    tweet,
    retweet_count,
    id_str,
    country,
    followers,
    language,
    my_table,
    my_database=DATABASE,
):
    """Populate a given table witht he Twitter collected data
    
    Args:
        user (str): username from the status
        created_at (datetime): when the tweet was created
        tweet (str): text
        retweet_count (int): number of retweets
        id_str (int): unique id for the tweet
    """

    dbconnect = connect_db(DATABASE)

    cursor = dbconnect.cursor()
    cursor.execute("USE airflowdb")

    query = f"INSERT INTO {my_table} (user, created_at, tweet, retweet_count, id_str, country, followers, language) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

    try:
        cursor.execute(
            query,
            (
                user,
                created_at,
                tweet,
                retweet_count,
                id_str,
                country,
                followers,
                language,
            ),
        )
        dbconnect.commit()
        print("commited")

    except mysql.Error as e:
        print(e)
        dbconnect.rollback()

    cursor.close()
    dbconnect.close()

    return


# ----------------------------------------------
#  Access the Twitter API
# ----------------------------------------------


def connectTwitter():
    config = ConfigParser()
    config.read(CONFIG_FILE)

    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(
        config.get("twitter", "consumer_key"), config.get("twitter", "consumer_secret")
    )
    auth.set_access_token(
        config.get("twitter", "access_token"),
        config.get("twitter", "access_token_secret"),
    )

    # Create Twitter API object
    twitter = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    print(f"🦄 Connected as {twitter.me().screen_name}")

    return twitter


class customListener(tweepy.StreamListener):
    """We need to create an instance of the Stream Listener
    http://docs.tweepy.org/en/v3.4.0/streaming_how_to.html      
    """

    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_data disconnects the stream
            return False

    def on_status(self, status):
        print(status.text)
        return True

    def on_data(self, data):
        """
        Automatic detection of the kind of data collected from Twitter
        This method reads in tweet data as Json and extracts the data we want.
        """
        try:
            # parse as json
            json_data = json.loads(data)

            # extract the relevant data
            if "text" in json_data:
                user = json_data["user"]["screen_name"]
                created_at = parser.parse(json_data["created_at"])
                tweet = json_data["text"]
                retweet_count = json_data["retweet_count"]
                id_str = json_data["id_str"]
                followers = json_data["user"]["followers_count"]
                language = json_data["user"]["lang"]
                if json_data["place"] is not None:
                    country = json_data["place"]["country"]
                else:
                    country = None

            # insert data just collected into MySQL my_database
            populate_table(
                user,
                created_at,
                tweet,
                retweet_count,
                id_str,
                country,
                followers,
                language,
                "tweets_long",
            )
            print(f"Tweet colleted at: {created_at}")

        except Error as e:
            print(e)


def start_stream(stream, **kwargs):
    """Start the stream, prints the disconnection error
    
    Args:
        stream (obj): stream object to start
    """
    try:
        stream.filter(**kwargs)
    except Exception:
        stream.disconnect()
        print("Fatal exception")


if __name__ == "__main__":

    create_table(DATABASE, "tweets_long")
    # first we need to authenticate
    twitter = connectTwitter()

    # next: create stream listener
    myStreamListener = customListener()
    myStream = tweepy.Stream(auth=twitter.auth, listener=myStreamListener, timeout=30)

    # stream tweets using the filter method
    version = float(f"{sys.version_info[0]}.{sys.version_info[1]}")
    if version >= 3.7:
        kwargs = {
            'track': ["python", "pycon", "jupyter", "#pycon2019"],
            'is_async': True
        }
    else:
        kwargs = {
            'track': ["python", "pycon", "jupyter", "#pycon2019"],
            'async': True
        }
        pass
    start_stream(myStream, **kwargs)
    pass
