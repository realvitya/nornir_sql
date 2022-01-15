Installation
============
.. note::
    It is advisable to create a separate virtual environment (venv) for your network automation framework!

Creating venv
-------------

.. code-block:: console

    python -m venv nornir-venv

Activating the new venv:

.. code-block:: console

    rem Windows:
    w:\nornir-venv\Scripts\activate

    # Linux:
    $ . nornir-venv/bin/activate

Installing nornir-sql
---------------------

.. include:: ../../README.rst
    :start-after: install_instructions
    :end-before: install_instructions_end

Installing SQL dependencies
---------------------------
Different SQL connectors need different drivers to have. As **nornir-sql** uses **SQLAlchemy** for database
operation, please check the relevant documentation for specifying your connection URL and installing your
dependecies as per `SQLAlchemy / Engine Configuration <https://docs.sqlalchemy.org/en/14/core/engines.html>`_
