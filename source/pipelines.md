# Pipelines

![](_static/automation1.jpg)

Automation helps us speed those manual boring tasks. The ability to automate means you can spend time working on other more thought-intensive projects.

Automation adds monitoring and logging tasks:

| **Easy to automate**                   | **Difficult to automate**           |
| -------------------------------------- | ----------------------------------- |
| Regularly scheduled reports            | One off or non-scheduled tasks      |
| Clear success / failure outcomes       | Unclear success / failure  outcomes |
| Input that can be handled via machines | Requires deeper human input         |


## Steps to automation

It is good to start with a checklist:
- When should this task begin?
- Does this taks have a time limit?
- What are the inputs for this task?
- What is success or failure within this task?
- If the task fails what should happen?
- What does the task provide or produce? In what way? To whom?
- What (if anything) should happen after the task concludes?

<div class="alert alert-primary">
  <h4> Top tip </h4>
  If your project is too large or loosely defined, try breaking it up into smaller tasks and automate a few of those tasks. Perhaps your task involves a report which downloads two datasets, runs cleanup and analysis, and then sends the results to different groups depending on the outcome. You can break this task into subtasks, automating each step. If any of these subtasks fail, stop the chain and alert the whoever is responsible for maintaining the script so it can be investigated further.
</div>

## What is a data pipeline?

Roughly this is how all pipelines look like:

![](https://i1.wp.com/datapipesoft.com/wp-content/uploads/2017/05/data-pipeline.png?fit=651%2C336&ssl=1)

they consist mainly of three distinct parts: data engineering processes, data preparation and analytics. The upstream steps and quality of data determines in great measure the performance and quality of the subsequent steps.

## Why do pipelines matter?

- Analytics and batch processing are mission critical as they power all data-intensive applications
- The complexity of the data sources and demands increase every day
- A lot of time is invested in writing, monitoring jobs, and troubleshooting issues.

This makes data engineering one of the most critical foundations of the whole analytics cycle.

### Good data pipelines are:

- Reproducible
- Easy to productise

When working with data pipelines the following two principles always apply:


![](_static/gooddata.png)

---

![](_static/gooddata1.png)

As your data engineering and data quality demands increase so does the complexity of the processes. So more often than not you will eventually need a workflow manager to help you with the orchestration of such processes.

<div class="alert alert-custom">
Think of a workflow manager as:

GNU Make + Unix pipes + Steroids
</div>


---

## Creating your first etl pipeline in Python


### Setting your local database

Let's us access your local MySQL from the command line, type the following on the command line:
```sh
mysql -u -root -p
```
followed by your MySQL password

you should see the following message as well as a change in your prompt:

```
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 276
Server version: 8.0.15 Homebrew

Copyright (c) 2000, 2019, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

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
We will need to create a new database for the following sections. So let's start by creating a new database called `airflow-tutorial`:

```sql
 CREATE DATABASE airflow-tutorial CHARACTER SET utf8 COLLATE utf8_unicode_ci;
 ```

as well as creating a corresponding user:
```sql
CREATE USER 'airflow'@'localhost' IDENTIFIED BY 'password';
```
make sure to substitute `password` with an actual password. Now we need to make sure that the `airflow` user has access to the database:
```sql
GRANT ALL PRIVILEGES ON *.* TO 'airflow'@'localhost';
FLUSH PRIVILEGES'
```

If you want to restrict the access of this user to the `airflow-tutorial` database for example you can do it via:
```sql
GRANT ALL PRIVILEGES ON airflow-tutorial.* To 'airflow'@'localhost';
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

if you need to remove an user you can use the following command;
```sql
DROP USER '<username>'@'localhost' ;
```

### Checking connection to the database from Python

The following snippet will allow you to connect to the created database from Python:

```python
# Script to check connection to the database we created earlier

# importing the connector from mysqlclient
import mysql.connector as mysql

# connecting to the database using the connect() method
# it takes 3 parameters: user, host and password

dbconnect = mysql.connect(host="localhost", user="airflow", password="python2019")

# print the connection object
print(dbconnect)

# do not forget to close the connection
dbconnect.close()

```

`dbconnect` is a  conection object which can be used to execute queries, commit transactions and rollback transactions before closing the connection.




