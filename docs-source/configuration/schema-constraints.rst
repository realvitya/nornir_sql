Schema constraints
==================
This inventory plugin was designed to work with any existing database and inventory loading is purely depends on
the queries.

The queries you define have some rules. You'll get exceptions while loading the inventory if these are not considered:

#. **hosts_query** must provide ``name`` and ``hostname`` at minimum!
#. **groups_query** must provide ``name``!
#. If **hosts_query** defines ``groups``, those group names must exists provided by the ``groups_query``!
#. ``groups`` provided by the **hosts_query** is a single group name or a coma separated list of groups.
#. All fields provided by the queries and not used by Nornir inventory data structure will be simply ignored!