"""
This module should require the admin role, but we
don't handle authentication yet.
"""
from flask import Blueprint, request

from result import *
from require import fields, response
from NgacApi.attribute import UserAttribute
from NgacApi.ngac import NGAC
from NgacApi.user import User


user = Blueprint("user", __name__, url_prefix="/user")


@user.route("/new", methods=["POST"])
@fields(request)
def make_user(user_id, attribute):
    """
    Creates a new user
    ---
    """
    ngac = NGAC(token=request.headers["token"])
    user = User([UserAttribute(attribute)], id=user_id)
    return ngac.add_user(user).match(
        lambda x: response("User created"),
        lambda x: response(f"Error {x.value}", code=400)
    )


@user.route("assign", methods=["POST"])
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


@user.route("unassign", methods=["POST"])
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
