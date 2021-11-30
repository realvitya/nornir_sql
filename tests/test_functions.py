"""tests.test_functions"""
from nornir.core.inventory import Host, Group

from nornir_sql.plugins.inventory.sql import _get_defaults, _get_connection_options


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
