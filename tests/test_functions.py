"""tests.test_functions"""
import pytest
from nornir.core.inventory import Host, Group, Inventory

from nornir_sql.plugins.inventory.sql import _get_defaults, _get_connection_options, SQLInventory
from sqlalchemy.exc import SQLAlchemyError, ArgumentError


def test_create_host(test_database):
    """Test host creation"""
    data = {"name": "testhost", "hostname": "testhostname", "data.data1": "data1value", "data.data2": "data2value"}
    result = {
        "name": "testhost",
        "hostname": "testhostname",
        "username": None,
        "password": None,
        "platform": None,
        "port": None,
        "groups": [],
        "data": {
            "data1": "data1value",
            "data2": "data2value",
        },
        "connection_options": {},
    }
    test_host: Host = test_database._get_inventory_element(Host, data=data)
    assert test_host.dict() == result


def test_create_host_with_extra_elements(test_database):
    """Test host creation with extra values which are not supported

    These fields should be ignored.
    """
    data = {
        "name": "testhost",
        "hostname": "testhostname",
        "data.data1": "data1value",
        "data.data2": "data2value",
        "someextra": "value",
    }
    result = {
        "name": "testhost",
        "hostname": "testhostname",
        "username": None,
        "password": None,
        "platform": None,
        "port": None,
        "groups": [],
        "data": {
            "data1": "data1value",
            "data2": "data2value",
        },
        "connection_options": {},
    }
    test_host: Host = test_database._get_inventory_element(Host, data=data)
    assert test_host.dict() == result


def test_create_group(test_database):
    """Test group creation"""
    data = {"name": "testgroup", "data.data1": "data1value", "data.data2": "data2value"}
    result = {
        "name": "testgroup",
        "hostname": None,
        "username": None,
        "password": None,
        "platform": None,
        "port": None,
        "groups": [],
        "data": {
            "data1": "data1value",
            "data2": "data2value",
        },
        "connection_options": {},
    }
    test_group: Group = test_database._get_inventory_element(Group, data=data)
    assert test_group.dict() == result


def test_get_connection_options():
    """Test get_connection_options function"""
    data = {
        "paramiko": {
            "hostname": "host1",
            "port": 22,
            "platform": "cisco_iosxe",
        }
    }
    result = {
        "extras": None,
        "hostname": "host1",
        "port": 22,
        "username": None,
        "password": None,
        "platform": "cisco_iosxe",
    }
    assert _get_connection_options(data)["paramiko"].dict() == result


def test_get_defaults():
    """Test _get_defaults function"""
    data = {
        "hostname": "host1",
        "port": "22",
        "platform": "cisco_iosxe",
        "data": {"source": "nornir_sql"},
        "connection_options": """{
                                      "paramiko": {
                                          "port": 222,
                                          "extras": {
                                              "extra1": "opt1"
                                           }
                                      }
                                 }
        """,
    }
    result = {
        "hostname": "host1",
        "username": None,
        "password": None,
        "port": "22",
        "platform": "cisco_iosxe",
        "data": {"source": "nornir_sql"},
        "connection_options": {
            "paramiko": {
                "extras": {"extra1": "opt1"},
                "hostname": None,
                "password": None,
                "platform": None,
                "port": 222,
                "username": None,
            }
        },
    }
    assert _get_defaults(data).dict() == result


@pytest.mark.slow
def test_database_load(test_database):
    """Testing of loading inventory from test sqlite database"""
    test_inventory: Inventory = test_database.load()
    hosts = [host.name for host in test_inventory.hosts.values()]
    # check if we have all hosts
    assert hosts == ["FW1", "FW2", "FW3", "SW1", "SW2", "SW3", "ROUTER1", "ROUTER2", "ROUTER3"]
    # check if data element is loaded and accessible
    assert test_inventory.hosts["FW1"]["region"] == "EA"


@pytest.mark.slow
def test_database_load_with_groups(test_database_with_groups):
    """Testing of loading inventory from test sqlite database"""
    test_inventory: Inventory = test_database_with_groups.load()
    hosts = [host.name for host in test_inventory.hosts.values()]
    groups = [group.name for group in test_inventory.groups.values()]
    # check if we have all hosts
    assert hosts == ["FW1", "FW2", "FW3", "SW1", "SW2", "SW3", "ROUTER1", "ROUTER2", "ROUTER3"]
    # check if we have all groups
    assert groups == ["HUBDP", "switch-password"]
    # check if recursive data resolution works
    assert test_inventory.hosts["FW1"]["city"] == "Budapest"


@pytest.mark.slow
def test_database_load_with_groups_file(test_database_with_groups_file):
    """Testing of loading inventory from test sqlite database"""
    test_inventory: Inventory = test_database_with_groups_file.load()
    hosts = [host.name for host in test_inventory.hosts.values()]
    groups = [group.name for group in test_inventory.groups.values()]
    test_group = test_inventory.groups["test"]
    # groups cannot be added during SQL loading when using groups_file. We may use this or transform function:
    test_inventory.hosts["SW1"].groups.add(test_group)
    # check if we have all hosts
    assert hosts == ["FW1", "FW2", "FW3", "SW1", "SW2", "SW3", "ROUTER1", "ROUTER2", "ROUTER3"]
    # check if we have all groups
    assert groups == ["ios", "iosxr", "nxos", "eos", "junos", "test"]
    # check if recursive data resolution works (somedata is coming from 'test' group)
    assert test_inventory.hosts["SW1"]["somedata"] == "somevalue"
    # check if connection_options was coming from group 'ios' which is child of 'test'
    assert test_inventory.hosts["SW1"].get_connection_parameters("netmiko").dict() == {
        "extras": {},
        "hostname": "SW1",
        "password": None,
        "platform": "cisco_ios",
        "port": None,
        "username": None,
    }


@pytest.mark.slow
def test_sqlalchemy_wrong_url(test_database_wrong_url):
    with pytest.raises(SQLAlchemyError):
        SQLInventory(test_database_wrong_url, "")


@pytest.mark.slow
def test_sqlalchemy_sql_exception(test_database_wrong_query):
    with pytest.raises(SQLAlchemyError):
        test_database_wrong_query.load()
