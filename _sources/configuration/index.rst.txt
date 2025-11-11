Plugin configuration
====================
The plugin takes options in order to configure what DB to use, what queries it should run to construct the inventory.
These options are the following:

.. include:: ../../README.rst
    :start-after: configuration_options_start
    :end-before: configuration_options_end

At minimum, **sql_connection** and **hosts_query** must be specified. Other options are optional.

Very minimal inventory setup:

.. code-block:: python

    from nornir.core import InitNornir
    inventory = {
        "plugin": "SQLInventory",
        "options": {
            "sql_connection": "sqlite:///asset.db",
            "hosts_query": "select name, hostname from hosts"
        }
    }
    nr = InitNornir(inventory=inventory)

.. toctree::
    :maxdepth: 1

    schema-constraints
    python-configuration
    yaml-configuration
    using-groups-file
