"""
This module is responsible for connection handling, and provide a high-level interface for the client to send requests
and receive responses from the server.
"""

from uuid import UUID
from http import client, cookies, HTTPStatus, HTTPMethod
from abc import ABC
import requests
import msgpack
from core import *


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


class ConfigServer(ABC):
    """
    This class represents a Wireguard configuration server.
    """

    def __init__(
            self,
            url: str
    ):
        self.url = url
        self.credential = None

    def user_authenticate(self, username: str, password: str):
        try:
            response = requests.post(
                url=self.url + "/login",
                data=msgpack.packb({
                    "username": username,
                    "password": password
                })
            )
            match response.status_code:
                case HTTPStatus.OK:
                    self.credential = response.cookies
                    return True
                # TODO: ADD DETAILED ERROR HANDLING
                case HTTPStatus.UNAUTHORIZED:
                    return False
                case HTTPStatus.INTERNAL_SERVER_ERROR:
                    return False
                case _:
                    return False
        except requests.exceptions.ConnectionError:
            return False

    def user_registration(self, username: str, password: str):
        try:
            response = requests.post(
                url=self.url + "/register",
                data=msgpack.packb({
                    "username": username,
                    "password": password
                })
            )
            match response.status_code:
                case HTTPStatus.CREATED:
                    return True
                case HTTPStatus.CONFLICT:
                    return False
                case HTTPStatus.INTERNAL_SERVER_ERROR:
                    return False
                case _:
                    return False
        except requests.exceptions.ConnectionError:
            return False

    def user_logout(self, username: str):
        try:
            response = requests.post(
                url=self.url + "/logout",
                data=msgpack.packb({
                    "username": username
                })
            )
            match response.status_code:
                case HTTPStatus.OK:
                    return True
                case HTTPStatus.UNAUTHORIZED:
                    return False
                case HTTPStatus.INTERNAL_SERVER_ERROR:
                    return False
                case _:
                    return False
        except requests.exceptions.ConnectionError:
            return False

    def user_authenticate_token(self, token: str):
        pass

    def get_user_profile(self, user_id: UUID):
        try:
            response = requests.get(
                url=self.url + "/user/" + str(user_id),
                cookies=self.credential
            )
            # todo
            match response.status_code:
                case HTTPStatus.OK:
                    pass  # todo
                case HTTPStatus.UNAUTHORIZED:
                    pass  # todo
                case HTTPStatus.NOT_FOUND:
                    pass  # todo
                case HTTPStatus.INTERNAL_SERVER_ERROR:
                    pass  # todo
                case _:
                    pass  # todo
        except requests.exceptions.ConnectionError:
            pass  # todo
        pass

    def update_user_profile(self, user_obj: user.User):
        pass

    def get_config(self, config_id: UUID):
        pass

    def create_config(self, config_obj: wgconfig.WireguardConfig):
        pass

    def get_network_object(self, network_uuid: UUID, objects: list[UUID]):
        pass

    def update_network_object(self, network_uuid: UUID, objects: list[wgobject.WireguardObject]):
        pass

    def join_network(self, network_uuid: UUID):
        pass

    def quit_network(self, network_uuid: UUID):
        pass
