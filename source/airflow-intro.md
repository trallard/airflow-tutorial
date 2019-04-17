# Introduction to Airflow

## What is Airflow?

![airflow logo](_static/airflow-logo.jpeg)

Airflow is a Workflow engine which means:

- Manage scheduling and running jobs and data pipelines
- Ensures jobs are ordered correctly based on dependencies
- Manage allocation of scarce resources
- Provides mechanisms for tracking the state of jobs and recovering from failure

## Basic Airflow concepts

- **Task**: defined unit of work
- **Task instance**: individual run of a single task
- **DAG**: Directed acyclic graph,
  a set of taks with explicit execution order, beginning and end
- **DAG run**: individual execution/run of a DAG

**Debunking the DAG**

The vertices and edges (the arrows linking the nodes) have an order and direction associated to them

![](_static/DAG.png)

each node in a DAG corresponds to a task, which in turn represents some sort of data processing. For example:

Node A could be the code for pulling data from an API, node B could be the code for anonymizing the data. Node B could be the code for checking that there are no duplicate records, and so on.

These 'pipelines' are acyclic since they need a point of completion.

**Dependencies**

Each of the vertices has a particular direction that shows the relationship between certain nodes. For example we can only anonymise data once this has been pulled out from the API.

## Idempotency

This is one of the most important characteristics of good ETL architectures.

When we say that something is idempotent it means it will produce the same result regardless of how many times this is run (i.e. the results are reproducbile).

Reproducibility is particularly imnportant in data-intensive environments as this ensures that same inputs will always return the same outputs.

## Airflow components

There are 4 main components to Apache Airflow:

### Webserver

The GUI. This is under the hood a Flask app where you can track the status of your jobs and read logs from a remote file store (e.g. [Azure Blobstorage](https://docs.microsoft.com/en-us/azure/storage/blobs/storage-blobs-overview/?wt.mc_id=PyCon-github-taallard)).

### Scheduler

This component is reponsible for scheduling the jobs. This is a multithreaded Pythonn process that uses the DAGb object to decide what tasks need to be run, when and where.

### Executor

The mechanism that gets the taks done.

### Metadata database

A database that powers how the other components interact. he scheduler stores and updates task statuses, which the webserver then uses to display job information.
