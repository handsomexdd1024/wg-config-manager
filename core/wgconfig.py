"""
Wireguard network configuration file, including:
- Network uuid
- Owner uuid
- User uuid list
- Config name
- WireguardNetwork uuid
"""

from abc import ABC, abstractmethod
from uuid import UUID
from core.wgobject import *


class WireguardNetworkConfig(ABC):
    """
    Wireguard network configuration file.
    """

    def __init__(
            self,
            identifier: UUID,
            name: str,
            owner: UUID,
            user_list: list[UUID],
            network_uuid: UUID
    ):
        """
        Initialize an application level Wireguard network config.
        :param identifier: uuid of the config file
        :param name: name of the config
        :param owner: owner of the config
        :param user_list: users participating in this network
        :param network_uuid: WireguardNetwork uuid
        """
        self.identifier = identifier
        self.name = name
        self.owner = owner
        self.user_list = user_list
        self.network_uuid = network_uuid

    # todo: add more possible objects and methods


def config_generator(
        network: WireguardNetwork,
        node_uuid: UUID
):
    pass  # todo: implement this function
