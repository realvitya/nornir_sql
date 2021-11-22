"""tests.conftest"""
import pytest

from nornir_sql.plugins.inventory import SQLInventory

hosts_query = """\
select UPPER(device_name) AS name,
       device_name AS hostname,
       dt.vendor || '_' || dt.os AS platform,
       dt.pid AS 'data.pid',
       r.name AS 'data.region'
from hosts_table ht
     inner join device_types dt on ht.device_type = dt.id
     inner join regions r on ht.region = r.id
where ht.status = 'deployed'
"""


hosts_query_with_groups = """\
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
"""

groups_query = """\
select name,
       platform,
       username,
       password,
       country AS 'data.country',
       city AS 'data.city'
from groups_table
"""

hosts_query_with_error = """\
select UPPER(device_nam) AS name,
       device_name AS hostname,
       dt.vendor || '_' || dt.os AS platform,
       dt.pid AS 'data.pid',
       r.name AS 'data.region'
from hosts_table ht
     inner join device_types dt on ht.device_type = dt.id
     inner join regions r on ht.region = r.id
where ht.status = 'deployed'
"""


@pytest.fixture
def test_database():
    return SQLInventory("sqlite:///sample/test.db", hosts_query=hosts_query)


@pytest.fixture
def test_database_with_groups():
    return SQLInventory("sqlite:///sample/test.db", hosts_query=hosts_query_with_groups, groups_query=groups_query)


@pytest.fixture
def test_database_wrong_query():
    return SQLInventory("sqlite:///sample/test.db", hosts_query=hosts_query_with_error)


@pytest.fixture
def test_database_wrong_url():
    return "sqlite://sample/test.db"
