====================
Nornir SQL Inventory
====================
Welcome to Nornir SQL inventory plugin!

If your device inventory is spread across SQL database tables and you would like to use it as Nornir inventory, you may
consider looking on this project.

------

| Documentation: `<https://realvitya.github.io/nornir_sql>`__
| Source code: `<https://github.com/realvitya/nornir_sql>`__

------

Installation
------------
.. install_instructions

Install from `pypi <https://pypi.org/project/nornir_sql>`__

.. code-block:: console

    pip install nornir-sql

Install from `GitHUB <https://github.com/realvitya/nornir_sql>`__

.. code-block:: console

    pip install git+https://github.com/realvitya/nornir_sql.git

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
This plugin is based on SQLAlchemy and supports all databases that SQLAlchemy does.

These configuration options can be used:

.. configuration_options_start

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
#. | ``groups_file``: path to a YAML file containing group definitions. Format is that same as used by
     ``SimpleInventory``
   | This parameter is ignored when ``groups_query`` or ``groups`` are specified!
   | Using this parameter requires group assignments outside of this plugin!
     Check `docs <https://realvitya.github.io/nornir_sql/configuration/using-groups-file.html#assigning-groups-to-hosts>`__!
#. | ``groups``: group definition as dict. Same restrictions and features apply as by using ``groups_file``!
   | Ignored when ``groups_query`` is specified!
   | Using this parameter requires group assignments outside of this plugin!
     Check `docs <https://realvitya.github.io/nornir_sql/configuration/using-groups-file.html#assigning-groups-to-hosts>`__!
#. | ``defaults``: This is a dictionary which contains inventory elements. These will be applied to hosts.

.. configuration_options_end
