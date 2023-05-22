"""
This module contains the network message format.
"""

__all__ = ["StandardResponse", "NetworkModification"]

from enum import Enum
from abc import ABC

import msgpack


class StandardResponse(ABC):
    """
    This class represents a standard response body from the server.
    """

    def __init__(
            self,
            code: int,
            message: str,
            content: bytes | None
    ):
        self.code = code
        self.message = message
        self.content = content

    @staticmethod
    def default_encoder(o):
        if isinstance(o, StandardResponse):
            return {
                "__StandardResponse__": True,
                "code": o.code,
                "message": o.message,
                "content": o.content
            }
        else:
            raise TypeError("Object is not a StandardResponse")

    @staticmethod
    def default_decoder(data: bytes) -> "StandardResponse":
        content = msgpack.unpackb(data)
        if isinstance(content, dict):
            return StandardResponse(
                code=content["code"],
                message=content["message"] if "message" in content else "",
                content=content["content"]
            )
        else:
            raise TypeError("Object is not a StandardResponse")


class NetworkModification(ABC):
    class Action:
        CREATE = 0
        DELETE = 1
        UPDATE = 2

    def __init__(self):
        self.action = None
        self.content = None
