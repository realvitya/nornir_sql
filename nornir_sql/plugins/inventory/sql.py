"""nornir_sql.plugins.inventory.sql"""
import json
import logging
from typing import Optional, Dict, Type, Any, Union

from nornir.core.inventory import (
    Inventory,
    Groups,
    Host,
    Group,
    ParentGroups,
    Hosts,
    HostOrGroup,
    Defaults,
    ConnectionOptions,
)
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger("nornir_sql")


def _get_connection_options(data: Union[str, Dict[str, Any]]) -> Dict[str, ConnectionOptions]:
    """Create per-platform ConnectionOptions objects from configuration dict

    Args:
        data (str|dict): Connection options in dict or JSON format

    Returns:
        dict of per-platform connection options
    """
    cp = {}
    if isinstance(data, str):  # convert json to dict
        data = json.loads(data)
    for cn, c in data.items():
        cp[cn] = ConnectionOptions(
            hostname=c.get("hostname"),
            port=c.get("port"),
            username=c.get("username"),
            password=c.get("password"),
            platform=c.get("platform"),
            extras=c.get("extras"),
        )
    return cp


def _get_defaults(data: Optional[Dict[str, Any]] = None) -> Defaults:
    if data is None:
        data = {}
    return Defaults(
        hostname=data.get("hostname"),
        port=data.get("port"),
        username=data.get("username"),
        password=data.get("password"),
        platform=data.get("platform"),
        data=data.get("data"),
        connection_options=_get_connection_options(data.get("connection_options", {})),
    )


class SQLInventory:
    """SQLInventory implements SQL inventory plugin for Nornir"""

    def __init__(
        self, sql_connection: str, hosts_query: str, groups_query: str = "", defaults: Optional[Dict[str, str]] = None
    ):
        """Setup SQLInventory parameters

        The SQL queries' fields must stick to the naming convention as follows:

        #. | ``name``: The device name in the inventory
        #. | ``hostname``: Device's hostname/fqdn/ip which is accessible
        #. | ``port``: Port on the device is accessible
        #. | ``username``: Username on the device
        #. | ``password``: Password on the device
        #. | ``platform``: Platform to use with the connection
        #. | ``data.extra1``: Will be put to ``data`` with the name of ``extra1``
        #. | ``groups``: Coma separated group names for this host
        #. | ``connection_options``: JSON formatted connection_options string

        Args:
            sql_connection (str): SQL connection string. E.g.: 'mssql+pymssql://@SERVERNAME/DBNAME'
            hosts_query (str): Query string for getting hosts. All fields must be named as above!
            groups_query (str): Query string for getting groups. All fields must be named as above!
            defaults (dict): dict of default values.
        """
        self.hosts_query: str = hosts_query
        self.groups_query: str = groups_query
        self.defaults: Defaults = _get_defaults(defaults)
        self.engine = None

        try:
            self.engine = create_engine(sql_connection)
        except SQLAlchemyError as err:
            logger.error(err)
            raise err from err

    def _get_inventory_element(self, typ: Type[HostOrGroup], data: Dict[str, str]) -> HostOrGroup:
        """Create a Host or Group object from dict

        Args:
            typ: Host or Group type
            data: dict of elements for the object

        Returns:
            Host or Group object
        """
        ret = typ(
            name=data.get("name"),
            hostname=data.get("hostname"),
            port=data.get("port"),
            username=data.get("username"),
            password=data.get("password"),
            platform=data.get("platform"),
            # ParentGroups object will be prepared after groups are loaded. Here we note the group names.
            groups=data["groups"].replace(" ", "").split(",") if data.get("groups") else [],
            data={extra.split(".")[1]: data.get(extra, "") for extra in data if "data." in extra},
            defaults=self.defaults,
            connection_options=_get_connection_options(data.get("connection_options", {})),
        )
        return ret

    def load(self) -> Inventory:
        """Load inventory from SQL server"""
        hosts = Hosts()
        groups = Groups()
        try:
            with self.engine.connect() as connection:
                results = connection.execute(self.hosts_query)

                for host_data in results:
                    host = self._get_inventory_element(Host, dict(host_data))
                    hosts[host.name] = host
                if self.groups_query:
                    results = connection.execute(self.groups_query)
                    for group_data in results:
                        group = self._get_inventory_element(Group, dict(group_data))
                        groups[group.name] = group
                    # replace strings to objects
                    for group in groups.values():
                        group.groups = ParentGroups([groups[g] for g in group.groups])
                    for host in hosts.values():
                        host.groups = ParentGroups([groups[g] for g in host.groups])
        except SQLAlchemyError as err:
            logger.error("SQL error: %s", err)
            raise err from err
        return Inventory(hosts=hosts, groups=groups, defaults=self.defaults)
