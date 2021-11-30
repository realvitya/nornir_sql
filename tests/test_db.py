"""tests.test_db"""
import pytest
from nornir.core.inventory import Inventory
from sqlalchemy.exc import SQLAlchemyError

from nornir_sql.plugins.inventory.sql import SQLInventory


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
def test_sqlalchemy_wrong_url(test_database_wrong_url):
    with pytest.raises(SQLAlchemyError):
        SQLInventory(test_database_wrong_url, "")


@pytest.mark.slow
def test_sqlalchemy_sql_exception(test_database_wrong_query):
    with pytest.raises(SQLAlchemyError):
        test_database_wrong_query.load()
