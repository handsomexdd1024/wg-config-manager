"""
This module contains the network message format.
"""

import json
from enum import Enum
from abc import ABC


class StandardResponse(ABC):
    """
    This class represents a standard response body from the server.
    """

    def __init__(
            self,
            code: int,
            message: str,
            content
    ):
        self.code = code
        self.message = message
        self.content = content


class NetworkModification:

    class Action:
        CREATE = 0
        DELETE = 1
        UPDATE = 2

    def __init__(self):
        self.action = None
        self.content = None
