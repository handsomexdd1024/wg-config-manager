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
from message_format import *


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
        self.session = requests.Session()

    def user_authenticate(self, username: str, password: str) -> (bool, UUID | None):
        try:
            if self.session.cookies:
                self.session.cookies.clear()
            http_response = self.session.post(
                url=self.url + "/login/pwd",
                data=msgpack.packb({
                    "username": username,
                    "password": password
                })
            )
            match http_response.status_code:
                case HTTPStatus.OK:
                    self.credential = http_response.cookies
                    if http_response.content:
                        std_response = StandardResponse.unpack(http_response.content)
                        if std_response.code == 0:
                            return True, UUID(bytes=std_response.content)
                        else:
                            return False, None
                case HTTPStatus.UNAUTHORIZED:
                    return False, None
                case HTTPStatus.INTERNAL_SERVER_ERROR:
                    return False, None
                case _:
                    return False, None
        except requests.exceptions.ConnectionError:
            return False, None
        # todo: add more error handling

    def user_registration(self, username: str, password: str) -> bool:
        try:
            response = self.session.post(
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

    def user_logout(self, username: str) -> bool:
        try:
            response = self.session.post(
                url=self.url + "/logout",
                data=msgpack.packb({
                    "username": username
                })
            )
            match response.status_code:
                case HTTPStatus.OK:
                    self.session.cookies.clear()
                    return True
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
            response = self.session.get(
                url=self.url + "/user/" + str(user_id),
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
        try:
            response = requests.get(
                url=self.url + "/config/" + str(config_id),
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
            pass

    def create_config(self, config_name: str):
        try:
            response = requests.post(
                url=self.url + "/config/new",
                cookies=self.credential,
                data=msgpack.packb({
                    "name": config_name
                })
            )
            # todo
            match response.status_code:
                case HTTPStatus.CREATED:
                    pass  # todo
                case HTTPStatus.UNAUTHORIZED:
                    pass  # todo
                case HTTPStatus.INTERNAL_SERVER_ERROR:
                    pass  # todo
                case _:
                    pass  # todo
        except requests.exceptions.ConnectionError:
            pass

    def get_network_object(self, network_uuid: UUID, object_uuid_list: list[UUID]):
        try:
            response = requests.get(
                url=self.url + "/network/" + str(network_uuid),
                cookies=self.credential,
                data=msgpack.packb({
                    "objects": object_uuid_list
                })
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
            pass

    def update_object(
            self,
            modification_list: list[message_format.NetworkModification],
            object_list: list[wgobject.NetworkObject]
    ):
        pass

    def join_network(self, network_uuid: UUID):
        pass

    def quit_network(self, network_uuid: UUID):
        pass
