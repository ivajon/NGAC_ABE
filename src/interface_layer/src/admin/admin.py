"""
This module should require the admin role, but we
don't handle authentication yet.
"""
from flask import Blueprint, request

from API.result import *
from NgacApi.ngac import NGAC
from NgacApi.policy import Policy


admin = Blueprint("admin", __name__, url_prefix="/admin")


def has_keys(keys, dictionary):
    """
    Checks if a dictionary has all the keys in a list
    ---
    """
    for key in keys:
        if key not in dictionary.keys():
            return Error(key)
    return Ok("")


@admin.route("/load_policy", methods=["POST"])
def load_policy():
    """
    Loads a policy from plaintext submitted by the admin
    ---
    """
    data = request.data
    if "token" not in request.headers.keys():
        return "No admin token provided"
    status = has_keys(["policy"], data)
    if status.is_err():
        return status.value
    ngac = NGAC(token=request.headers["token"])

    pol = data["policy"]
    return ngac.load_policy_from_str(pol).match(
        lambda x: f"{x}",
        lambda x: f"Error {x.value}",
    )


@admin.route("/revoke_access", methods=["POST"])
def revoke_access():
    """
    Revokes access to a resource for a user
    ---
    """
    data = request.data
    if "token" not in request.headers.keys():
        return "No admin token provided"
    status = has_keys(["user_id", "attribute"], data)
    if status.is_err():
        return status.value
    ngac = NGAC(token=request.headers["token"])

    user_id = data["user_id"]
    attribute = data["attribute"]
    # return ngac.remove(, attribute).match(
    # No remove method in ngac
    return "Not implemented"


@admin.route("/add_user_attribute", methods=["POST"])
def add_user_attribute():
    """
    Adds an attribute to a user
    ---
    """
    data = request.data
    if "token" not in request.headers.keys():
        return "No admin token provided"
    status = has_keys(["user_id", "attribute"], data)
    if status.is_err():
        return status.value
    ngac = NGAC(token=request.headers["token"])

    user_id = data["user_id"]
    attribute = data["attribute"]
    # Not implemented
    return "Not implemented"
