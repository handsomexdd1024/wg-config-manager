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

    def pack(self):
        return msgpack.packb({
            "uuid": self.uuid.bytes,
            "name": self.name,
            "hashed_password": self.hashed_password,
            "salt": self.salt
        })

    @staticmethod
    def unpack(data: bytes):
        content = msgpack.unpackb(data)
        if isinstance(content, dict):
            return User(
                identifier=uuid.UUID(bytes=content["uuid"]),
                name=content["name"],
                hashed_password=content["hashed_password"],
                salt=content["salt"]
            )
        else:
            return None

    def authenticate(self, plaintext: str) -> bool:
        return bcrypt.checkpw(plaintext.encode("bytes"), self.hashed_password)
