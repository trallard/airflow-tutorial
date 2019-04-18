# Airflow 101

## Getting Airflow set up on your local computer 

### Pre-requisites
The following prerrequisites are needed:

- Libraries detailed in the Setting up section (either via conda or pipenv)
- mysql installed and running
  
## Getting your environment up and running

If you followed the instructions you should have Airflow installed. So let's get our environment up and running:

If you are using conda start your environment via:
```
source activate airflow-env
```

If using pipenv then:
```
pipenv shell
````
this will start a shell within a virtual environment.



Airflow home lives in `~/airflow` by default, but you can change the location of this. From the command line:

```
export AIRFLOW_HOME=~/airflow

# install from pypi using pip
pip install apache-airflow
```

you should see something like this in the `airflow` dir:

```
drwxr-xr-x    - tania 18 Apr 14:02 .
.rw-r--r--  26k tania 18 Apr 14:02 ├── airflow.cfg
drwxr-xr-x    - tania 18 Apr 14:02 ├── logs
drwxr-xr-x    - tania 18 Apr 14:02 │  └── scheduler
drwxr-xr-x    - tania 18 Apr 14:02 │     ├── 2019-04-18
lrwxr-xr-x   46 tania 18 Apr 14:02 │     └── latest -> /Users/tania/airflow/logs/scheduler/2019-04-18
.rw-r--r-- 2.5k tania 18 Apr 14:02 └── unittests.cfg
```

the next thing to do is run
` airflow initdb` this will initialize your database via alembic so that it matches the latest Airflow release.
This database will be used to track what has as has not been completed.

Let's edit the `airflow.config` document since Airflow uses `sqlite` databes which is normally outgrown very quickly as you cannot parallelize tasks using this database.

By now you should have `mysql` installed and `mysqlclient` installed.

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
