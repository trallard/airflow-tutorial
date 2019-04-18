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

## Why do pipelines matter?

- Analytics and batch processing are mission critical as they power all data-intensive applications
- The complexity of the data sources and demands increase every day
- A lot of time is invested in writing, monitoring jobs, and troubleshooting issues.

### Good data pipelines are:

- Reproducible
- Easy to productise

![](_static/gooddata.png)

![](_static/gooddata1.png)

 You need a workflow manager

<div class="alert alert-custom">
Think:

GNU Make + Unix pipes + Steroids
</div>
