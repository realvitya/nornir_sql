.. _using-groups:

Using groups
============
If you wanted to specify your group definitions as a dict or as a YAML file instead of the SQL DB, you can use
``groups`` or ``groups-file`` parameter by inventory configuration. The format of the data is exactly the same as
of the ``SimpleInventory`` plugin.

.. warning::
    When you define groups, you have to assign the group objects to the hosts after
    inventory was loaded!

In the following groups file we set couple of connection parameters for different plugins.
After assigning the correct group we can use all of these plugins to connect to devices.

.. literalinclude :: ../../sample/groups.yaml
   :language: yaml

Assigning groups to hosts
-------------------------
As hosts are not referencing the groups upon loading them from SQL, we have to do the assignment after
all hosts and groups are loaded. We cannot use ``transform function`` because we cannot reference groups
while loading a particular host.

Here is a solution to define a group assignment function:

.. code-block:: python

   from nornir.core import Nornir

   def assign_groups(nr: Nornir):
    groups = nr.inventory.groups
    for host in nr.inventory.hosts.values():
        # put whatever logic to assign groups
        if "WS-C" in host['pid']:
            host.groups.add(groups["ios"])
        elif "SRX" in host['pid']:
            host.groups.add(groups["junos"])
   ...
   nr = InitNornir(inventory=inventory)
   assign_groups(nr)

   # check if we got the connection parameters
   print(nr.inventory.hosts["SW1"].get_connection_parameters("netmiko").dict())
