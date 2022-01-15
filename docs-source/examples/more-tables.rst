SQLite example with multiple tables and groups
==============================================
In this example we will use a more complex table structure to build our Nornir inventory.

The full data structure with test data can be found here: :ref:`Test DB`

Query to gather hosts from more tables
--------------------------------------
The query below will gather hosts and construct ``platform`` based on other fields. We also store some additional
data like PID and region. Notice that we use multiple tables to store these data so we use join.

.. code-block:: sql
    :caption: hosts_query

    select UPPER(device_name) AS name,
           device_name AS hostname,
           dt.vendor || '_' || dt.os AS platform,
           dt.pid AS 'data.pid',
           r.name AS 'data.region',
           groups
    from hosts_table ht
         inner join device_types dt on ht.device_type = dt.id
         inner join regions r on ht.region = r.id
    where ht.status = 'deployed'

Query to get groups
-------------------
The above hosts query contained groups field. In database we must store coma separated values which point to a
name in the following query.

.. code-block:: sql
    :caption: groups_query

    select name,
           platform,
           username,
           password,
           country AS 'data.country',
           city AS 'data.city'
    from groups_table
