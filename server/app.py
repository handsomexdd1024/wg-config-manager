"""
This module defines the HTTP API server.
"""


import msgpack
from uuid import UUID, uuid4
from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Welcome to the Server!<p>"


@app.route("/login/pwd", methods=["POST"])
def login_pwd():

    # obtain data
    data = msgpack.unpackb(request.data, raw=False)

    # extract username and password
    username = data.get("username")
    password = data.get("password")

    # todo: user authenticate

    # todo: generate token, set cookie


@app.route("/signup", methods=["POST"])
def user_signup():
    data = msgpack.unpackb(request.data, raw=False)
    username = data.get("username")
    password = data.get("password")

    # todo: validate username and password

    # todo: add user info


@app.route("/logout", methods=["POST"])
def user_logout():
    data = msgpack.unpackb(request.data, raw=False)
    uuid = UUID(bytes=data.get("uuid"))
    username = data.get("username")

    # todo: invalidate token


@app.route("/user/<user_id>", methods=["GET", "POST"])
def user_profile(user_id):
    pass


@app.route("/config/<config_id>", methods=["GET", "POST"])
def config_profile(config_id):
    pass


@app.route("/network/<network_id>", methods=["GET", "POST"])
def network_profile(network_id):
    pass


@app.route("/network/<network_id>/object", methods=["GET", "POST"])
def network_object(network_id):
    pass
