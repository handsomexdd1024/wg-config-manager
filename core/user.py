# Copyright (c) 2023 Billy Yang.
# This software is licensed under the GNU AGPLv3 license.

"""
User module for WireGuard configuration management system.
"""

from abc import ABC, abstractmethod
import bcrypt
import uuid


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

    def authenticate(self, plaintext: str) -> bool:
        return bcrypt.checkpw(plaintext.encode("bytes"), self.hashed_password)
