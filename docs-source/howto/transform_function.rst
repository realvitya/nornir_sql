I have no platform information in DB. How can I set it?
=======================================================
If platform information is not saved directly in the asset database, still you can set the **platform** later
after DB read is done. You can do hat by defining a so called transform function. That function will be called
on every host object in your inventory after the DB load. The function can alter the data stored for each host.

What that transform function do depends on what information you have in the database.

Example1 - using naming convention
----------------------------------
For example you have naming convention like this: SITE-TYPE-NUMBER

examples:
    * HOU-SW-01
    * BDP-FW-01
    * MSC-RTR-01

You know that a switch can only be a junos, firewall should be panos and router is cisco ios, then this is a sample
code for you:

.. code-block:: python

    from nornir.core.plugins.inventory import TransformFunctionRegister

    def complete_host_data(host: Host, arg1: str = ""):
        """Transform function to set platform for hosts

        Args:
            host (Host): host object passed by Nornir
            arg1 (str): just an example argument you can use in your function

        Returns:
            None
        """
            if "-SW-" in host.name:
                host.platform = "juniper_junos"
            elif "-FW-" in host.name:
                host.platform = "palo_panos"
            elif "-RTR-" in host.name:
                host.platform = "cisco_ios"

    # make Nornir aware of your function
    TransformFunctionRegister.register("complete_host_data", complete_host_data)

    # setup inventory configuration
    inventory = {
        "plugin": "SQLInventory",
        "options": {
            "sql_connection": "......",
            "hosts_query": "......",
        },
        "transform_function": "complete_host_data",           # your function name
        "transform_function_options": {"arg1": "somevalue"},  # arguments for the function (optional)
    }

Example2 - using DB data
------------------------
Your asset info may contain product number (PID) for your devices.
You may use this query:

.. code-block:: SQL

    SELECT name, hostname, product_number AS 'data.pid' FROM asset

So you could use this minimalistic transform function:

.. code-block:: python

    def complete_host_data(host: Host):
        """Transform function to set platform for hosts"""
        if "ASA" in host['pid']:
            host.platform = "cisco_asa"
        elif "WS-C" in host['pid']:
            host.platform = "cisco_ios"
        elif "SRX" in host['pid']:
            host.platform = "juniper_junos"
