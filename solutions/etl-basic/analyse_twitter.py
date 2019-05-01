import os
import os.path
import re
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import mysql.connector as mysql
import numpy as np
import pandas as pd

# import the previously created functions
from stream_twitter import connect_db

# Details for our MySql connection
DATABASE = {
    "host": "localhost",
    "user": "airflow",
    "password": "python2019",
    "db": "airflowdb",
}

# ----------------------------------------------
#  Database related functions
# ----------------------------------------------


def sql_to_csv(my_database, my_table):

    dbconnect = connect_db(my_database)

    cursor = dbconnect.cursor()

    query = f"SELECT * FROM {table}"
    all_tweets = pd.read_sql_query(query, dbconnect)

    if os.path.exists("./data"):
        all_tweets.to_csv("./data/raw_tweets.csv", index=False)

    else:
        os.mkdir("./data")
        all_tweets.to_csv("./data/raw_tweets.csv", index=False)


def sql_to_df(my_database, my_table):
    dbconnect = connect_db(my_database)

    cursor = dbconnect.cursor()

    query = f"SELECT * FROM {my_table}"

    # store in dataframe

    df = pd.read_sql_query(query, dbconnect, index_col="id")

    cursor.close()
    dbconnect.close()

    return df


# ----------------------------------------------
#  Data processing
# ----------------------------------------------


def clean_data(df):

    # Make all usernames lowercase
    clean_df = df.copy()
    clean_df["user"] = df["user"].str.lower()

    # keep only non RT
    clean_df = clean_df[~clean_df["tweet"].str.contains("RT")]

    return clean_df


def create_plots(df):
    x = df["language"].unique()
    fig, ax = plt.subplots()
    countries = df["language"].value_counts()
    plt.bar(range(len(countries)), countries)
    fig.suptitle("Language counts")
    plt.xlabel("languages")
    plt.ylabel("count")
    ax.set_xticklabels(x)

    if os.path.exists("./plots"):
        fig.savefig("./plots/barchart_lang.png")

    else:
        os.mkdir("./plots")
        fig.savefig("./plots/barchart_lang.png")


def save_df(df):
    today = datetime.today().strftime("%Y-%m-%d")

    if os.path.exists("./data"):
        df.to_csv(f"./data/{today}-clean-df.csv", index=None)

    else:
        os.mkdir("./data")
        df.to_csv(f"./data/{today}-clean-df.csv", index=None)


if __name__ == "__main__":

    df = sql_to_df(DATABASE, "tweets_long")
    print("Database loaded in df")

    clean_df = clean_data(df)

    create_plots(clean_df)

    save_df(clean_df)
