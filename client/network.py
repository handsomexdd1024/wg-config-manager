"""
This module is responsible for connection handling, and provide a high-level interface for the client to send requests
and receive responses from the server.
"""

from abc import ABC
from http import HTTPStatus
from uuid import UUID

import msgpack
import requests

from core import *
from core.message_format import *


class ConfigServer(ABC):
    """
    This class represents a Wireguard configuration server.
    """

    def __init__(
            self,
            url: str
    ):
        self.url = url
        self.session = requests.Session()

    @classmethod
    def response_handler(
            cls,
            response: requests.Response,
            success_responses=None
    ) -> tuple[bool, StandardResponse]:
        if success_responses is None:
            success_responses = [HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.ACCEPTED]
        if response.status_code in success_responses:
            return True, StandardResponse.default_decoder(response.content)

    def user_auth_request(self, username: str, password: str) -> [bool, UUID | str]:
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
            app_response = self.response_handler(http_response)
            if app_response[0]:
                return True, UUID(bytes=app_response[1].content)
            else:
                return False, app_response[1].message
        except requests.exceptions.ConnectionError:
            return False, "Connection error"

    def user_signup_request(self, username: str, password: str) -> [bool, None | str]:
        try:
            http_response = self.session.post(
                url=self.url + "/register",
                data=msgpack.packb({
                    "username": username,
                    "password": password
                })
            )
            app_response = self.response_handler(http_response)
            if app_response[0]:
                return True, None
            else:
                return False, app_response[1].message
        except requests.exceptions.ConnectionError:
            return False, "Connection error"

    def user_logout_request(self, username: str) -> (bool, str | None):
        try:
            response = self.session.post(
                url=self.url + "/logout",
                data=msgpack.packb({
                    "username": username
                })
            )
            app_response = self.response_handler(response)
            if app_response[0]:
                self.session.cookies.clear()
                return True, None
            else:
                return False, app_response[1].message
        except requests.exceptions.ConnectionError:
            return False, "Connection error"

    def get_user_profile(self, user_id: UUID) -> [bool, user.User | str]:
        try:
            http_response = self.session.get(
                url=self.url + "/user/" + str(user_id),
            )
            app_response = self.response_handler(http_response)
            if app_response[0]:
                return True, user.User.default_decoder(app_response[1].content)
            else:
                return False, app_response[1].message
        except requests.exceptions.ConnectionError:
            return False, "Connection error"

    def update_user_profile(self, user_obj: user.User):
        pass

    def get_config(self, config_id: UUID) -> [bool, wgconfig.WireguardConfig | str]:
        try:
            http_response = self.session.get(
                url=self.url + "/config/" + str(config_id),
            )
            # todo
            app_response = self.response_handler(http_response)
            if app_response[0]:
                return True, wgconfig.WireguardConfig.default_decoder(app_response[1].content)
            else:
                return False, app_response[1].message
        except requests.exceptions.ConnectionError:
            pass

    def create_config(self, config_name: str):
        try:
            http_response = self.session.post(
                url=self.url + "/config/new",
                data=msgpack.packb({
                    "name": config_name
                })
            )
            app_response = self.response_handler(http_response)
            if app_response[0]:
                pass  # todo: complete api design
            else:
                return False, app_response[1].message
        except requests.exceptions.ConnectionError:
            return False, "Connection error"

    def get_network_object(self, network_uuid: UUID, object_uuid_list: list[UUID]) \
            -> [bool, list[wgobject.WireguardObject] | str]:
        try:
            http_response = self.session.get(
                url=self.url + "/network/" + str(network_uuid) + "/object",
                data=msgpack.packb({
                    "object_uuid_list": [object_id.bytes for object_id in object_uuid_list]
                })
            )
            app_response = self.response_handler(http_response)
            if app_response[0]:
                pass  # todo: design object decoding mechanism
            else:
                return False, app_response[1].message
        except requests.exceptions.ConnectionError:
            return False, "Connection error"

    def update_object(
            self,
            modification_list: list[message_format.NetworkModification],
            object_list: list[wgobject.WireguardObject]
    ) -> [bool, None | str]:
        try:
            http_response = self.session.post(
                url=self.url + "/object/update",
                data=msgpack.packb({
                    "modification_list": modification_list,
                    "object_list": object_list
                })
            )
            app_response = self.response_handler(http_response)
            if app_response[0]:
                return True, None
            else:
                return False, app_response[1].message
        except requests.exceptions.ConnectionError:
            return False, "Connection error"

    def join_network(self, network_uuid: UUID) -> [bool, None | str]:
        try:
            http_response = self.session.post(
                url=self.url + "/network/" + str(network_uuid) + "/join",
            )
            app_response = self.response_handler(http_response)
            if app_response[0]:
                return True, None
            else:
                return False, app_response[1].message
        except requests.exceptions.ConnectionError:
            return False, "Connection error"

    def quit_network(self, network_uuid: UUID):
        try:
            http_response = self.session.post(
                url=self.url + "/network/" + str(network_uuid) + "/quit",
            )
            app_response = self.response_handler(http_response)
            if app_response[0]:
                return True, None
            else:
                return False, app_response[1].message
        except requests.exceptions.ConnectionError:
            return False, "Connection error"
