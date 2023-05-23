__all__ = ["ObjectLoader"]

import client.network
from core import *
from abc import ABC
from uuid import UUID
from enum import Enum


class ObjectLoader(ABC):
    """
    Object cache and loader, providing interfaces for the main process to load Wireguard Objects.
    Refreshes cache when needed, or when refresh() is called.
    """

    def __init__(self):
        self._cache = {}

    def __setitem__(self, index: UUID, o: wgobject.WireguardObject):
        self._cache[index] = o

    def __getitem__(self, index: UUID):
        return self._cache[index]

    def __delitem__(self, index: UUID):
        del self._cache[index]

    def __contains__(self, index: UUID):
        return index in self._cache

    def __len__(self):
        return len(self._cache)

    def refresh(self):
        """
        Refresh the cache.
        :return: None
        """
        pass
