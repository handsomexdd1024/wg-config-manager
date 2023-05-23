"""
This module loads configuration from the given config file path.
"""

import os
import yaml


class Config:
    def __init__(self, path: str):
        self.path = path
        if not os.path.exists(path):
            raise FileNotFoundError("Config file not found.")
        with open(path, "r") as f:
            config = yaml.load(f, yaml.CFullLoader)
        try:
            self.listen_address = config["listen_address"]
            self.listen_port = config["listen_port"]
            self.db_url = config["db_url"]
            self.db_user = config["db_user"]
            self.db_pwd = config["db_pwd"]
        except KeyError:
            raise ValueError("Config file is not valid.")
