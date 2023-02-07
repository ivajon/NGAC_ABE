"""
This module should require the admin role, but we
don't handle authentication yet.
"""
from flask import Blueprint, request

from result import *
from require import fields, response
from NgacApi.ngac import NGAC
from NgacApi.policy import Policy
from .user import user
from .object import resource
from . import url, set_current_policy, get_policy

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
    if "Token" not in request.headers.keys():
        return "No admin token provided", 404
    ngac = NGAC(token=request.headers["token"], policy_server_url=url)

    if is_error(ngac.load_policy_from_str(policy)):
        return response("Invalid policy", code=400)

    def save_policy():
        set_current_policy(policy_name)
        return "Policy loaded", 200

    ret = ngac.change_policy(Policy(name=policy_name))
    return ret.match(
        lambda x: save_policy(),
        lambda x: response(f"Error {x.value}", code=400)
    )


@admin.route("/read_policy", methods=["POST"])
def read_policy():
    ngac = NGAC(token=request.headers["token"], policy_server_url=url)
    pol = Policy(name=get_policy())
    ret = ngac.read(policy=pol)
    return ret.match(
        ok=lambda x: (x, 200),
        error=lambda x: (f"Error {x.value}", 400)
    )
