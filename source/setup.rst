Getting started
===============
This section will guide you through the pre requisites for the workshop:

Python
++++++

We will be using `Python <https://www.python.org/>`_.
Installing all of Python's research packages individually can be a bit
difficult, so we recommend using `Anaconda <https://www.anaconda.com/>`_ which
provides a variety of useful packages/tools.

To download Anaconda, follow the link https://www.anaconda.com/download/ and select
Python 3. Following the download, run the installer as per usual on your machine.

Git
+++

`Git <https://git-scm.com/>`_ is a version control software that records changes
to a file or set of files. Git is especially helpful for software developers
as it allows changes to be tracked (including who and when) when working on a
project.

To download Git, go to the following link and choose the correct version for your
operating system: https://git-scm.com/downloads.

GitHub
++++++

GitHub is a web-based service for version control using Git. You will need
to set up an account at `https://github.com <https://github.com>`_. Basic GitHub accounts are
free and you can now also have private repositories.

Text Editors
++++++++++++

Text editors are tools with powerful features designed to optimize writing code.
There are several text editors that you can choose from.
Here are some we recommend:

- `VS code <https://code.visualstudio.com//?wt.mc_id=pyconCZ-github-taallard>`_: this is our favourite

- `Atom <https://atom.io>`_

- `Pycharm <https://www.jetbrains.com/pycharm/download/>`_


We suggest trying several editors before settling on one.

If you decide to go for VSCode make sure to also
have the `Python extension <https://marketplace.visualstudio.com/itemdetails?itemName=ms-python.python/?wt.mc_id=PyCon-github-taallard>`_
installed. This will make your life so much easier.


Azure
+++++

You will need to get an Azure account as we will be using this to deploy the 
Airflow instance.

Follow `this link <https://azure.microsoft.com/en-us/free//?wt.mc_id=PyCon-github-taallard>`_ 
to get an Azure free subscription. This will give you 150 dollars in credit so you
can get started.

If you are doing this tutorial live at PyCon US then your
facilitator will provide you with specific instructions to set up your Azure 
subscription. If you have not received these please let your facilitator know ASAP.


Additional libraries
+++++++++++++++++++++

We will be using the following libraries:

- airflow
- pandas
- azure-cli
- matplotlib

If you are using Anaconda you can use this `environment.yaml` and install the 
dependencies via ``conda env create -f environment.yml``.

If you are using pipenv then use this `Pipfile` and install via ``pipenv install``.

Finally you can install the libraries via pip `pip install -r requirements.txt`

Please make sure to install all the dependencies before the tutorial as the WiFi 
at the conferences venue cannot always be trusted.
