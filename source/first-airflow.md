# Airflow 101: working locally and familiarise with the tool

### Pre-requisites

The following prerrequisites are needed:

- Libraries detailed in the Setting up section (either via conda or pipenv)
- mysql installed
- text editor
- command line
  
## Getting your environment up and running

If you followed the instructions you should have Airflow installed as well as the rest of the packages we will be using. 

So let's get our environment up and running:

If you are using conda start your environment via:
```
$ source activate airflow-env
```
If using pipenv then:
```
$ pipenv shell
````

this will start a shell within a virtual environment, to exit the shell you need to type `exit` and this will exit the virtual environment.

## Starting Airflow locally

Airflow home lives in `~/airflow` by default, but you can change the location before installing airflow. You first need to set the `AIRFLOW_HOME` environment variable and then install airflow. For example using pip:

```sh
export AIRFLOW_HOME=~/mydir/airflow

# install from pypi using pip
pip install apache-airflow
```

once you have completed the installation you should see something like this in the `airflow` directory (wherever it lives for you)

```
drwxr-xr-x    - myuser 18 Apr 14:02 .
.rw-r--r--  26k myuser 18 Apr 14:02 ├── airflow.cfg
drwxr-xr-x    - myuser 18 Apr 14:02 ├── logs
drwxr-xr-x    - myuser 18 Apr 14:02 │  └── scheduler
drwxr-xr-x    - myuser 18 Apr 14:02 │     ├── 2019-04-18
lrwxr-xr-x   46 myuser 18 Apr 14:02 │     └── latest -> /Users/myuser/airflow/logs/scheduler/2019-04-18
.rw-r--r-- 2.5k myuser 18 Apr 14:02 └── unittests.cfg
```
We need to create a local dag folder:

```
mkdir ~/airflow/dags
```

As your project evolve, your directory will look something like this:

```
airflow                  # the root directory.
├── dags                 # root folder for all dags. files inside folders are not searched for dags.
│   ├── my_dag.py        # my dag (definitions of tasks/operators) including precedence.
│   └── ...
├── logs                 # logs for the various tasks that are run
│   └── my_dag           # DAG specific logs
│   │   ├── src1_s3      # folder for task specific logs (log files are created by date of run)
│   │   ├── src2_hdfs
│   │   ├── src3_s3
│   │   └── spark_task_etl
├── airflow.db           # SQLite database used by Airflow internally to track status of each DAG.
├── airflow.cfg          # global configuration for Airflow (this can be overriden by config inside the file.)
└── ...
```

## Prepare your database

As we mentioned before Airflow uses a database to keep track of the tasks and their statuses. So it is critical to have one set up.

To start the default database we can run
` airflow initdb`. This will initialize your database via alembic so that it matches the latest Airflow release.

The default database used is `sqlite` which means you cannot parallelize tasks using this database. Since we have mysql and mysqlclient installed we will set them up so that we can use them with airflow.

🚦Create an airflow database

From the command line:

```
mysql -u root -p
mysql> CREATE DATABASE airflow CHARACTER SET utf8 COLLATE utf8_unicode_ci;
mysql> create user 'airflow'@'localhost' identified by 'airflow';
mysql> grant all privileges on * . * to 'airflow'@'localhost';
mysql> flush privileges;
```
and inititalize the database:

```
airflow initdb
```

## Update your local configuration

Open your airflow configuration file `~/airflow/airflow.cf` and make the following changes;

```
executor = CeleryExecutor
sql_alchemy_conn = mysql://airflow:airflow@localhost:3306/airflow
broker_url = amqp://guest:guest@localhost:5672/
```

Here we are replacing the default executor (`SequentialExecutor`) with the `CeleryExecutor` so that we can run multiple DAGs in parallel.
We also replace the default `sqlite` database with our newly created `

Let's now start the webserver locally:


```
airflow webserver -p 8080
```

we can head over to [http://localhost:8080](http://localhost:8080) now and you will see that there are a number of example DAGS already there.

🚦 Take some time to familiarise with the UI and get your local instance set up

Now let's have a look at the connections ([http://localhost:8080/admin/connection/](http://localhost:8080/admin/connection/)) go to `admin > connections`. You should be able to see a number of connection availables. For this tutorial we will use some of the connections including  `mysql`.

For example if you have `mysql` running but you have a different password for the root user you can edit it by clicking on the connection name.


🚦Now let's create a db for our local project

![](_static/connection.png)


Let us go over some of the commands. Back on your command line:

```
airflow list_dags
```
we can list the DAG tasks in a tree view

```
airflow list_tasks tutorial --tree
```

we can tests the dags too, but we will need to set a date parameter so that this executes:

```
airflow test tutorial print_date 2019-05-01
```
(note that you cannot use a future date or you will get an error)
```
airflow test tutorial templated 2019-05-01
```
By using the test commands theese are not saved in the database.

Now let's start the scheduler:
```
airflow scheduler
```
and now with the scheduler up and running we can trigger an instance:
```
$ airflow run airflow run example_bash_operator runme_0 2015-01-01
```

This will be stored in the database and you can see the  change of the status change straight away.

What would happen for example if we wanted to run  or trigger the `tutorial` task? 🤔

Let's try from the UI and see what happens.

```
airflow trigger_dag tutorial
```


## Writing your first DAG

Let's create our first simple DAG. 
Inside the dag directory (`~/airflow/dags)` create a `simple_dag.py` file.

And let's start by importing the needed libraries:

```python
# airflow related
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
# other packages
from datetime import datetime
from datetime import timedelta
```

Next we need to set the defaults: