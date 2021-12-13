YAML configration
=================
It's possible to store configuration data in external YAML files instead of Python code. The structure must
follow the dictionary format though.

The previous :ref:`Python configuration` chapter describe the following YAML format:

.. code-block:: YAML
   :caption: config.yaml

   ---
   inventory:
        plugin: SQLInventory
        options:
            sql_connection: 'mssql+pymssql://user:password@DBSERVER/DATABASE'
            hosts_query: >
                SELECT [CI name] AS name, hostname, groups
                FROM hosts
                WHERE status = 'deployed'
            groups_query: >
                SELECT name, platform
                FROM groups
                WHERE platform != ''
            defaults:
                username: 'my_user'
                password: 'my_password'
                connection_options:
                    scrapli:
                        platform: 'cisco_iosxe'
                        extras:
                            ssh_config_file: True
                            auth_strict_key: False

Then you can use this file by the initialization:

.. code-block:: python

   from nornir import InitNornir
   nr = InitNornir(config_file="config.yaml")

