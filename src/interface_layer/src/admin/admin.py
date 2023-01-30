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
    ngac = NGAC(token=request.headers["token"])

    if ngac.load_policy_from_str(policy).is_err():
        return response("Invalid policy", code=400)

    return ngac.change_policy(Policy(name=policy_name)).match(
        lambda x: response("Policy loaded"),
        lambda x: response(f"Error {x.value}", code=400)
    )


@admin.route("/read_policy", methods=["POST"])
def read_policy():
    ngac = NGAC(token=request.headers["token"])
    return ngac.read().match(
        lambda x: response(x.value),
        lambda x: response(f"Error {x.value}", code=400)
    )
