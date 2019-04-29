# Airflow basics

## What is Airflow?

![airflow logo](_static/airflow-logo.jpeg)

Airflow is a Workflow engine which means:

- Manage scheduling and running jobs and data pipelines
- Ensures jobs are ordered correctly based on dependencies
- Manage the allocation of scarce resources
- Provides mechanisms for tracking the state of jobs and recovering from failure

It is highly versatile and can be used across many many domains:
![](_static/uses.png)

## Basic Airflow concepts

- **Task**: a defined unit of work (these are called operators in Airflow)
- **Task instance**: an individual run of a single task. Task instances also have an indicative state, which could be “running”, “success”, “failed”, “skipped”, “up for retry”, etc.
- **DAG**: Directed acyclic graph,
  a set of tasks with explicit execution order, beginning, and end
- **DAG run**: individual execution/run of a DAG

**Debunking the DAG**

The vertices and edges (the arrows linking the nodes) have an order and direction associated to them

![](_static/DAG.png)

each node in a DAG corresponds to a task, which in turn represents some sort of data processing. For example:

Node A could be the code for pulling data from an API, node B could be the code for anonymizing the data. Node B could be the code for checking that there are no duplicate records, and so on.

These 'pipelines' are acyclic since they need a point of completion.

**Dependencies**

Each of the vertices has a particular direction that shows the relationship between certain nodes. For example, we can only anonymize data once this has been pulled out from the API.

## Idempotency

This is one of the most important characteristics of good ETL architectures.

When we say that something is idempotent it means it will produce the same result regardless of how many times this is run (i.e. the results are reproducible).

Reproducibility is particularly important in data-intensive environments as this ensures that the same inputs will always return the same outputs.

## Airflow components

![](_static/architecture.png)

There are 4 main components to Apache Airflow:

### Web server

The GUI. This is under the hood a Flask app where you can track the status of your jobs and read logs from a remote file store (e.g. [Azure Blobstorage](https://docs.microsoft.com/en-us/azure/storage/blobs/storage-blobs-overview/?wt.mc_id=PyCon-github-taallard)).

### Scheduler

This component is responsible for scheduling jobs. This is a multithreaded Python process that uses the DAGb object to decide what tasks need to be run, when and where.

The task state is retrieved and updated from the database accordingly. The web server then uses these saved states to display job information.

### Executor

The mechanism that gets the tasks done.

### Metadata database

Let's us access your local MySQL from the command line, type the following on the command line:
```sh
MySQL -u root -p
```
followed by your MySQL password (this was done as part of your setup)

## Workflow as a code
One of the main advantages of using a workflow system like Airflow is that all is code, which makes your workflows maintainable, versionable, testable, and collaborative.

Thus your workflows become more explicit and maintainable (atomic tasks).

Not only your code is dynamic but also is your infrastructure.

### Defining tasks

Tasks are defined based on the abstraction of `Operators` (see Airflow docs [here](https://airflow.apache.org/concepts.html#operators)) which represent a single **idempotent task**.

mysql>
```
 To see the existing databases you can use the following command:
 ```sql
 SHOW DATABASES
 ```
 you can also see the users and the relevant hosts using the following command
 ```sql
 SELECT user, host, FROM mysql.user;
 ```
We will need to create a new database for the following sections. So let's start by creating a new database called `airflowdb`:

```sql
 CREATE DATABASE airflowdb CHARACTER SET utf8 COLLATE utf8_unicode_ci;
 ```

Examples:

```python
t1 = BashOperator(task_id='print_date',
    bash_command='date,
    dag=dag) 
```

If you want to restrict the access of this user to the `airflowdb` database, for example, you can do it via:
```sql
GRANT ALL PRIVILEGES ON airflowdb.* To 'airflow'@'localhost';
FLUSH PRIVILEGES;
```

 
 so now the output of ` SELECT user, host, FROM mysql.user;` should look like this:

 ```sql
 mysql> select user, host FROM mysql.user;
+------------------+-----------+
| user             | host      |
+------------------+-----------+
| airflow          | localhost |
| mysql.infoschema | localhost |
| mysql.session    | localhost |
| mysql.sys        | localhost |
| root             | localhost |
+------------------+-----------+
5 rows in set (0.00 sec)
```

if you need to remove a user you can use the following command:
```sql
DROP USER '<username>'@'localhost' ;
```

### 🚦Checking connection to the database from Python

The following snippet will allow you to connect to the created database from Python:

Note that you need the database name, password and user for this.

```python
# Script to check the connection to the database we created earlier airflowdb


# connecting to the database using the connect() method
# it takes 3 parameters: user, host, and password

dbconnect = mysql.connect(host="localhost", 
                          user="airflow", 
                          password="python2019", 
                          db="airflowdb")

# print the connection object
print(dbconnect)

# do not forget to close the connection
dbconnect.close()

```

`dbconnect` is a  connection object which can be used to execute queries, commit transactions and rollback transactions before closing the connection. We will use it more later.

The `dbconnect.close()` method is used to close the connection to database. To perform further transactions, we need to create a new connection.


### Streaming Twitter data into the database

### Airflow
- Airbnb data teaam
- Open-sourced mud 2015
- Apache incubator mid 2016
- ETL pipelines

### Similarities
- Python open source projects for data pipelines
- Integrate with a number of sources (databases, filesystems)
- Tracking failure, retries, success
- Ability to identify the dependencies and execution

### Differences
- Scheduler support: Airflow has built in support using schedulers
- Scalability: Airflow has had stability issues in the past
- Web interfaces

🚦 The first step will be to create a config file (`config.cgf`) with your Twitter API tokens.
```
[twitter]
consumer_key = xxxxxxxxxxxxxxxxxx
consumer_secret = xxxxxxxxxxxxxxxxxx 
access_token = xxxxxxxxxxxxxxxxxx
access_token_secret = xxxxxxxxxxxxxxxxxx 
```
Now to the coding bits:


![](_static/airflow.png)


config = ConfigParser()
config.read(CONFIG_FILE)

# Authenticate to Twitter
auth = tweepy.OAuthHandler(
    config.get("twitter", "consumer_key"), config.get("twitter", "consumer_secret")
)
auth.set_access_token(
    config.get("twitter", "access_token"), config.get("twitter", "access_token_secret")
)

# Create Twitter API object
twitter = tweepy.API(auth)

# let's collect some of the tweets in your public timeline
public_tweets = twitter.home_timeline()

for tweet in public_tweets:
    print(tweet.text)
```

### 🚦 Create a new table

Let us create a folder called `etl basic` and an `stream_twitter.py` script in it. 
This table will contain the following:
- username
- tweet content
- time of creation
- retweet count
- place 
- location

We need to create a new table for the Twitter data. This corresponds to 6 columns and the primary key.




### 🚦 Collect Tweets

The Twitter Streaming API has [rate limits](https://dev.twitter.com/streaming/overview/connecting), and prohibits too many connection attempts happening too quickly. It also prevents too many connections being made to it using the same authorization keys. Thankfully, tweepy takes care of these details for us, and we can focus on our program.

The main thing that we have to be aware of is the queue of tweets that we’re processing. If we take too long to process tweets, they will start to get queued, and Twitter may disconnect us. This means that processing each tweet needs to be extremely fast.



Let's us transform the connection script we created before:
```python
# Import libraries needed
import json
import time

from configparser import ConfigParser
from pathlib import Path

import tweepy
from dateutil import parser
from mysql import connector as mysql

# Path to the config file with the keys make sure not to commit this file
CONFIG_FILE = Path.cwd() / "config.cfg"

def connectTwitter():
    config = ConfigParser()
    config.read(CONFIG_FILE)

    # Authenticate to Twitter
    
    # Create Twitter API object
    twitter = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    # display some info on the authentication
    print()

    return twitter
```

The next step is to create a stream listener.

The `StreamListener` class has a method called on_data. This method will automatically figure out what kind of data Twitter sent, and call an appropriate method to deal with the specific data type. It’s possible to deal with events like users sending direct messages, tweets being deleted, and more. 

```python
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
            raw_data = json.loads(data)

            # extract the relevant data
            if "text" in raw_data:
                user = raw_data["user"]["screen_name"]
                created_at = parser.parse(raw_data["created_at"])
                tweet = raw_data["text"]
                retweet_count = raw_data["retweet_count"]
                location = raw_data["user"]["location"]

            if raw_data["place"] is not None:
                place = raw_data["place"]["country"]
            else:
                place = None

            # insert data just collected into MySQL database
            # populateTable(user, created_at, tweet, retweet_count, location, place)
            print(f"Tweet colleted at: {created_at}")

        except Error as e:
            print(e)
```

🚦 So for this to be called we need to wrap around a main function:

```python
if __name__ == "__main__":
```

🚀 So far we have collected some data through streaming (enough to collect some data). And created a database where this data is going to be deposited into.

The next step is to transform the data and prepare it for more downstrem processes.

There are different mechanisms to share data between pipeline steps:

- files 
- databases
- queues

In each case, we need a way to get data from the current step to the next step.

### Extending your data pipeline

