"""
Wireguard network configuration file, including:
- Network uuid
- Owner uuid
- User uuid list
- Config name
- WireguardNetwork uuid
"""

__all__ = ["WireguardConfig", "config_generator"]

from abc import ABC, abstractmethod
from uuid import UUID
from core.wgobject import *


class WireguardConfig(ABC):
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

    @staticmethod
    def default_encoder(o):
        if isinstance(o, WireguardConfig):
            return {
                "__WireguardConfig__": True,
                "uuid": o.identifier.bytes,
                "name": o.name,
                "owner": o.owner.bytes,
                "user_list": [i.bytes for i in o.user_list],
                "network_uuid": o.network_uuid.bytes
            }
        else:
            raise ValueError("Not a WireguardConfig object.")

    @staticmethod
    def default_decoder(o):
        if "__WireguardConfig__" in o:
            return WireguardConfig(
                identifier=UUID(bytes=o["uuid"]),
                name=o["name"],
                owner=UUID(bytes=o["owner"]),
                user_list=[UUID(bytes=i) for i in o["user_list"]],
                network_uuid=UUID(bytes=o["network_uuid"])
            )
        else:
            raise ValueError("Not a WireguardConfig object.")


def config_generator(
        network: WireguardNetwork,
        node_uuid: UUID
):
    pass  # todo: implement this function
