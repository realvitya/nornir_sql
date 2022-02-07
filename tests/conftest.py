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
def test_database_with_groups_sql():
    return SQLInventory("sqlite:///sample/test.db", hosts_query=hosts_query_with_groups, groups_query=groups_query)


@pytest.fixture
def test_database_wrong_query():
    return SQLInventory("sqlite:///sample/test.db", hosts_query=hosts_query_with_error)


@pytest.fixture
def test_database_wrong_url():
    return "sqlite://sample/test.db"


@pytest.fixture
def test_database_with_groups_file():
    return SQLInventory("sqlite:///sample/test.db", hosts_query=hosts_query, groups_file="sample/groups.yaml")


@pytest.fixture
def test_database_with_groups_dict():
    groups = {
        "ios": {
            "platform": "ios",
            "connection_options": {
                "netmiko": {"platform": "cisco_ios", "extras": {}},
                "scrapli": {"platform": "cisco_iosxe", "extras": {}},
                "napalm": {"platform": "ios", "extras": {"optional_args": {}}},
            },
        },
        "iosxr": {
            "platform": "iosxr",
            "connection_options": {
                "netmiko": {"platform": "cisco_xr", "extras": {}},
                "scrapli": {"platform": "cisco_iosxr", "extras": {}},
                "napalm": {"platform": "iosxr", "extras": {"optional_args": {}}},
            },
        },
        "nxos": {
            "platform": "nxos",
            "connection_options": {
                "netmiko": {"platform": "cisco_nxos_ssh", "extras": {}},
                "scrapli": {"platform": "cisco_nxos", "extras": {}},
                "napalm": {"platform": "nxos_ssh", "extras": {"optional_args": {}}},
            },
        },
        "eos": {
            "platform": "eos",
            "connection_options": {
                "netmiko": {"platform": "arista_eos", "extras": {"global_delay_factor": 1}},
                "scrapli": {"platform": "arista_eos", "extras": {}},
                "napalm": {"platform": "eos", "extras": {"optional_args": {}}},
            },
        },
        "junos": {
            "platform": "junos",
            "connection_options": {
                "netmiko": {"platform": "juniper_junos", "extras": {}},
                "scrapli": {"platform": "juniper_junos", "extras": {}},
                "napalm": {"platform": "junos", "extras": {"optional_args": {}}},
            },
        },
        "test": {"groups": ["ios"], "data": {"somedata": "somevalue"}},
    }

    return SQLInventory("sqlite:///sample/test.db", hosts_query=hosts_query, groups=groups)
