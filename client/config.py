"""
Load client configuration.
"""
from abc import ABC, abstractmethod
import yaml


class Config(ABC):
    def __init__(self, path: str):
        with open(path, "r") as f:
            config = yaml.load(f, yaml.CFullLoader)
        try:
            self.server_url = config["server_url"]
        except KeyError:
            raise ValueError("Config file is not valid.")
