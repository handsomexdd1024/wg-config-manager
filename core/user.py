# Copyright (c) 2023 Billy Yang.
# This software is licensed under the GNU AGPLv3 license.

"""
User module for WireGuard configuration management system.
"""

from abc import ABC, abstractmethod
import bcrypt
import uuid

import msgpack


class User(ABC):
    """
    This class represents a user.
    """

    def __init__(
            self,
            identifier: uuid.UUID,
            name: str,
            hashed_password: bytes,
            salt: bytes
    ):
        self.name = name
        self.uuid = identifier
        self.hashed_password = hashed_password
        self.salt = salt

    @staticmethod
    def default_decoder(o):
        if "__User__" in o:
            return User(
                uuid.UUID(bytes=o["uuid"]),
                o["name"],
                o["hashed_password"],
                o["salt"]
            )
        else:
            return None  # todo: raise error

    @staticmethod
    def default_encoder(o):
        if isinstance(o, User):
            return {
                "__User__": True,
                "uuid": o.uuid.bytes,
                "name": o.name,
                "hashed_password": o.hashed_password,
                "salt": o.salt
            }
        else:
            return None

    def authenticate(self, plaintext: str) -> bool:
        return bcrypt.checkpw(plaintext.encode("bytes"), self.hashed_password)
