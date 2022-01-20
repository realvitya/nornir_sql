Simple SQLite example with hosts table only
===========================================
In this example we will utilize a single hosts table to build our Nornir inventory.

Simple DB schema
----------------
Let's say we have this simple table containing all our info:

.. code-block:: sql

    CREATE TABLE "hosts_table" (
        `device_name`	TEXT,
        `region`	INTEGER,
        `groups`	TEXT,
        `status`	TEXT,
        `last_scanned`	TEXT
    )

Query to gather hosts
---------------------
The query below will gather hosts and assigns **cisco_ios** as platform for all hosts.

.. code-block:: sql

    SELECT
           device_name AS name,
           device_name AS hostname,
           'cisco_ios' AS platform
    FROM hosts_table

Please notice the field names are **name**, **hostname** and **platform**!

The minimum requirement is to have **name** and **hostname**. All other fields are optional for Nornir.
Of course you will need to complete your inventory upon initialization in order to fill in all required
information which other plugins and tasks use.

.. note::

    If your platform is not stored and you don't want to set it statically like in the above example,
    check out :ref:`I have no platform information in DB. How can I set it?`
