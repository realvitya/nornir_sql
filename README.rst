====================
Nornir SQL Inventory
====================
Welcome to Nornir SQL inventory plugin!

If your device inventory is spread across SQL database tables and you would like to use it as Nornir inventory, you may
consider looking on this project.

------

| Documentation: TDB
| Source code: `<https://github.com/viktorkertesz/nornir_sql>`__

------

Installation
------------
.. install_instructions

Install from pipy

.. code-block:: console

    pip install nornir-sql

Install from `GitHUB <https://github.com/viktorkertesz/nornir_sql>`__

.. code-block:: console

    pip install git+https://github.com/viktorkertesz/nornir_sql.git

Install from GitHUB clone for development

.. code-block:: console

    git clone https://github.com/viktorkertesz/nornir_sql.git
    cd nornir_sql
    pip install -e .[dev]

.. install_instructions_end

Simple example
--------------

.. code-block:: python

    from nornir import InitNornir

    host_query = """\
    SELECT ciname AS name, ip AS hostname, region AS 'data.region'
    FROM host_table
    WHERE status='deployed'
    """

    inventory = {
        "plugin": "SQLInventory",
        "options": {
            "sql_connection": "sqlite:///inventory.db",
            "hosts_query": hosts_query,
        }
    }

    nr = InitNornir(inventory=inventory)
    print(nr.inventory.hosts['FW1']['region'])

Configuration
-------------
.. configuration

This plugin is based on SQLAlchemy and supports all databases that SQLAlchemy does.

These configuration options can be used:

#. | ``sql_connection``: SQLAlchemy connection string
   | Format: ``{driver}://[user]:[password]@{DBSERVER}/{DATABASE}``
   | SQLite example:
   | ``sqlite:///somedb.db``
   | MSSQL example with domain user authentication:
   | ``mssql+pymssql://ACME\\dbuser:verysecret@DBSRV1/INFRA``
#. | ``hosts_query``: Select statement which returns hosts inventory elements.
   | The select must return at minimum the ``name`` field!
   | Field names must match the expected Nornir inventory elements!
   | The ``data`` elements are expected in ``data.[element]`` format. Quotation is needed!
   | If ``groups`` are returned, the following ``groups_query`` also has to be specified!
#. | ``groups_query``: Select statement which returns groups inventory elements.
   | Same requirements apply as for the ``hosts_query``.
#. | ``defaults``: This is a dictionary which contains inventory elements. These will be applied to hosts.

.. configuration_end