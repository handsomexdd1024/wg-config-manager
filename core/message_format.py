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
            content: bytes
    ):
        self.code = code
        self.message = message
        self.content = content

    def pack(self):
        return msgpack.packb({
            "code": self.code,
            "message": self.message,
            "content": self.content
        })

    @staticmethod
    def unpack(data: bytes):
        content = msgpack.unpackb(data)
        if isinstance(content, dict):
            return StandardResponse(
                code=content["code"],
                message=content["message"] if "message" in content else "",
                content=content["content"]
            )
        else:
            return None


class NetworkModification:

    class Action:
        CREATE = 0
        DELETE = 1
        UPDATE = 2

    def __init__(self):
        self.action = None
        self.content = None
