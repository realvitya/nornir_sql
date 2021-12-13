Python configuration
====================
You can assemble your configuration in a Python program by constructing a dictionary of the inventory configuration.

This is a general example of a configuration.

.. note:: groups and defaults are optional

.. code-block:: python

    hosts_query = """\
    SELECT [CI name] AS name, hostname, groups
    FROM hosts
    WHERE status = 'deployed'
    """

    groups_query = """\
    SELECT name, platform
    FROM groups
    WHERE platform != ''
    """

    defaults = {
        "username": "my_user",
        "password": "my_password",
        "connection_options": {
            "scrapli": {
               "platform": "cisco_iosxe",
               "extras": {
                    "ssh_config_file": True,
                    "auth_strict_key": False
               }
            }
        }
    }

    inventory = {
        "plugin": "SQLInventory",
        "options": {
            "sql_connection": "mssql+pymssql://user:password@DBSERVER/DATABASE"
            "hosts_query": hosts_query,
            "groups_query": groups_query,
            "defaults": defaults,
        }
    }

    nr = InitNornir(inventory=inventory)

The above example will load the inventory and it will set certain defaults as well.

.. tip:: **connection_options** can be stored in the database as well in a JSON text format!

    Name it as ``'data.connection_options'`` in the query!