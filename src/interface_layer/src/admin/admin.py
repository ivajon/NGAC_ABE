"""
This module should require the admin role, but we
don't handle authentication yet.
"""
from flask import Blueprint, request

from result import *
from require import fields, response, admin as admin_route
from NgacApi.attribute import UserAttribute, ObjectAttribute
from NgacApi.ngac import NGAC
from NgacApi.user import User
from NgacApi.resource import Resource
from NgacApi.policy import Policy


admin = Blueprint("admin", __name__, url_prefix="/admin")


@admin.route("/load_policy", methods=["POST"])
@admin_route()
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


@admin.route("user/assign", methods=["POST"])
@admin_route()
@fields(request)
def assign(user_id, attribute):
    """
    Assign attributes to users and resources
    ---
    """
    ngac = NGAC(token=request.headers["token"])
    attr = UserAttribute(attribute)
    user = User([attr], id=user_id)

    return ngac.assign(user, attr).match(
        lambda x: response("Attribute assigned"),
        lambda x: response(f"Error {x.value}", code=400)
    )


@admin.route("user/unassigned", methods=["POST"])
@admin_route()
@fields(request)
def user_unassign(user_id, attribute):
    """
    Remove attributes from a user
    ---
    """
    ngac = NGAC(token=request.headers["token"])
    attr = UserAttribute(attribute)
    user = User([attr], id=user_id)

    return ngac.remove_assignment(user, attr).match(
        lambda x: response("Attribute unassigned"),
        lambda x: response(f"Error {x.value}", code=400)
    )


@admin.route("object/assign", methods=["POST"])
@admin_route()
@fields(request)
def object_assign(object_id, attribute):
    """
    Assign attributes to a resource
    ---
    """
    ngac = NGAC(token=request.headers["token"])
    attr = ObjectAttribute(attribute)
    object = Resource([attr], id=object_id)

    return ngac.assign(object, attr).match(
        lambda x: response("Attribute assigned"),
        lambda x: response(f"Error {x.value}", code=400)
    )


@admin.route("object/unassigned", methods=["POST"])
@admin_route()
@fields(request)
def object_unassign(object_id, attribute):
    """
    Remove attributes from a resource
    ---
    """
    ngac = NGAC(token=request.headers["token"])
    attr = ObjectAttribute(attribute)
    object = Resource([attr], id=object_id)

    return ngac.remove_assignment(object, attr).match(
        lambda x: response("Attribute unassigned"),
        lambda x: response(f"Error {x.value}", code=400)
    )
