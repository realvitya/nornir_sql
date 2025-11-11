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
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from pathlib import Path
import ruamel.yaml

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
        self,
        sql_connection: str,
        hosts_query: str,
        groups_query: str = "",
        groups_file: Optional[str] = None,
        groups: Optional[dict] = None,
        defaults: Optional[Dict[str, str]] = None,
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
            groups_file (str): YAML file path to group definition file. Ignored when groups_query or groups are specified!
            groups (dict): group definition as dict. Ignored when groups_query is specified!
            defaults (dict): dict of default values.
        """
        self.hosts_query: str = hosts_query
        self.groups_query: str = groups_query
        if groups_file:
            self.groups_file: Optional[Path] = Path(groups_file).expanduser()
        else:
            self.groups_file: Optional[Path] = None
        self.groups: dict = groups
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
        if isinstance(data.get("groups"), list):
            # groups come from groups_file
            groups = data["groups"]
        else:
            # groups come from sql as a string
            groups = data["groups"].replace(" ", "").split(",") if data.get("groups") else []
        if isinstance(data.get("data"), dict):
            # extra data come from groups_file
            extra_data = data["data"]
        else:
            # extra data is provided by SQL
            extra_data = {extra.split(".")[1]: data.get(extra, "") for extra in data if "data." in extra}
        ret = typ(
            name=data.get("name"),
            hostname=data.get("hostname"),
            port=data.get("port"),
            username=data.get("username"),
            password=data.get("password"),
            platform=data.get("platform"),
            # ParentGroups object will be prepared after groups are loaded. Here we note the group names.
            groups=groups,
            data=extra_data,
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
                results = connection.execute(text(self.hosts_query))

                for host_data in results:
                    # Convert Row object to dictionary for SQLAlchemy 2.0 compatibility
                    host_dict = {column: host_data[i] for i, column in enumerate(results.keys())}
                    host = self._get_inventory_element(Host, host_dict)
                    hosts[host.name] = host
                if self.groups_query:
                    results = connection.execute(text(self.groups_query))
                    for group_data in results:
                        # Convert Row object to dictionary for SQLAlchemy 2.0 compatibility
                        group_dict = {column: group_data[i] for i, column in enumerate(results.keys())}
                        group = self._get_inventory_element(Group, group_dict)
                        groups[group.name] = group
                elif self.groups:
                    for n, g in self.groups.items():
                        group_data = {"name": n, **g}
                        group = self._get_inventory_element(Group, group_data)
                        groups[group.name] = group
                elif self.groups_file:
                    yml = ruamel.yaml.YAML(typ="safe")
                    if self.groups_file.exists():
                        with open(self.groups_file) as fi:
                            groups_dict = yml.load(fi) or {}
                        for n, g in groups_dict.items():
                            group_data = {"name": n, **g}
                            group = self._get_inventory_element(Group, group_data)
                            groups[group.name] = group

                if len(groups) > 0:
                    # replace strings to objects
                    for group in groups.values():
                        group.groups = ParentGroups([groups[g] for g in group.groups])
                    for host in hosts.values():
                        host.groups = ParentGroups([groups[g] for g in host.groups])
        except SQLAlchemyError as err:
            logger.error("SQL error: %s", err)
            raise err from err
        return Inventory(hosts=hosts, groups=groups, defaults=self.defaults)
