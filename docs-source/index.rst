Welcome to Nornir SQL inventory plugin!
=======================================

If your device inventory is spread across SQL database tables and you would like to use it as Nornir inventory, you may
consider looking on this project.

Features
--------
* database type independent (SQLAlchemy works under the hood)
* database schema independent (queries must be constructed in a specific way)
* group support directly from the DB (separate group query can provide general attributes)
* asset is not restricted to one specific table, queries can join tables

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   Overview <self>
   installation/index
   configuration/index
   examples/index
   howto/index
   contribute/index
   nornir_sql/index
