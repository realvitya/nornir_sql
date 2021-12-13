Workflow of contribution
========================
It is preferred to fork the project on GitHUB, do checkout develop branch and create pull request for the project
in order to merge your update.

Forking the project
-------------------
First, please fork the project to have it under your GitHUB account! In order to do it, click on the **Fork** button on
the upper right hand side.

Let's say you have account name ``helpfuluser``.

Install working environment
---------------------------
Install the project from GitHUB clone for development

.. code-block:: console

    git clone https://github.com/helpfuluser/nornir_sql.git
    cd nornir_sql
    git checkout develop
    pip install -e .[dev]

This will install the project along with some tool which will be needed to generate docs or do packaging.

Checks after your update is done
--------------------------------
The project uses ``invoke`` to ease your work on running certain checks or updates. You can list all the options you have
by the command ``invoke --list``

.. code-block:: console

    (venv36) D:\Projects\nornir_sql>invoke --list
    Available tasks:

      black     Run black PEP8 formatter
      build     Build wheel and source packages as preparation for pypi deployment
      clean     Cleanup working directory
      linters   Run all linters
      mkdocs    Compile docs
      publish   Build and publish on PyPi
      pylint    Run pylint linter
      test      Run pytest tester

If you changed Python code, please run ``invoke linters`` before committing and initiating pull requests! If any problem
is shown, please fix that and re-run linters!

If you updated docs, please run ``invoke mkdocs`` to generate documentation into docs folder! Do not add docs folder
files to develop branch as it is maintained in gh-pages branch online documentation system.

Push and pull request
---------------------
After all checks are done and everything looks ok, you are good to go ahead and push your commits to GitHUB.

When that push happened, go to your GitHUB page in this repository and the option to initiate a pull request will pop up.
There you can create the PR and from there the project maintainers will get notified about your contribution.
