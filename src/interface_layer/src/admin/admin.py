"""
This module should require the admin role, but we
don't handle authentication yet.
"""
from flask import Blueprint, request

from result import *
from require import fields, response
from NgacApi.ngac import NGAC
from NgacApi.policy import Policy
from .user import user, set_current_policy as set_user_policy
from .object import resource
from configparser import ConfigParser
from . import url

current_policy = None


def set_current_policy(policy):
    global current_policy
    set_user_policy(policy)

    current_policy = policy


admin = Blueprint("admin", __name__, url_prefix="/admin")
admin.register_blueprint(user)
admin.register_blueprint(resource)


@admin.route("/load_policy", methods=["POST"])
@fields(request)
def load_policy(policy, policy_name):
    """
    Loads a policy from plaintext submitted by the admin
    ---
    """
    if "token" not in request.headers.keys():
        return "No admin token provided"
    global url
    ngac = NGAC(token=request.headers["token"], policy_server_url=url)

    if ngac.load_policy_from_str(policy).is_err():
        return response("Invalid policy", code=400)

    def save_policy():
        global current_policy
        current_policy = policy_name
        return Ok("Policy loaded")
    return ngac.change_policy(Policy(name=policy_name)).match(
        lambda x: save_policy(),
        lambda x: response(f"Error {x.value}", code=400)
    )


@admin.route("/read_policy", methods=["POST"])
def read_policy():
    global url, current_policy
    ngac = NGAC(token=request.headers["token"], policy_server_url=url)
    pol = Policy(name=current_policy)
    ret = ngac.read(policy=pol)
    return ret.match(
        ok=lambda x: (x, 200),
        error=lambda x: (f"Error {x.value}", 400)
    )
