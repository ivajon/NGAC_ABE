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
from NgacApi.parser import parse
from NgacApi.policy import Policy
from . import url, current_policy

user = Blueprint("user", __name__, url_prefix="/user")


@user.route("/new", methods=["POST"])
@fields(request)
def make_user(user_id, attribute):
    """
    Creates a new user
    ---
    """
    global url
    ngac = NGAC(token=request.headers["token"], policy_server_url=url)
    user = User([UserAttribute(attribute)], id=user_id)
    return ngac.add_user(user).match(
        lambda x: response("User created"),
        lambda x: response(f"Error {x.value}", code=400)
    )


@user.route("/attributes", methods=["post"])
@fields(request)
def attributes(user_id):
    global url
    ngac = NGAC(token=request.headers["token"], policy_server_url=url)
    global current_policy
    pol = ngac.read(Policy(name=current_policy))
    if is_error(pol):
        return "Could not read policy from server", 400
    pol = unwrap(pol).split("\n")
    ret = parse(pol)
    ret = ret["user"][user_id]
    if ret:
        return str(ret)
    return "No such user", 400


@user.route("/assign", methods=["POST"])
@fields(request)
def assign(user_id, attribute):
    """
    Assign attributes to users and resources
    ---
    """
    global url
    ngac = NGAC(token=request.headers["token"], policy_server_url=url)
    attr = UserAttribute(attribute)
    user = User([attr], id=user_id)
    global current_policy
    return ngac.assign(user, attr, target_policy=current_policy).match(
        lambda x: "Attribute assigned",
        lambda x: (f"Error {x.value}", 400)
    )


@user.route("/unassign", methods=["POST"])
@fields(request)
def unassign(user_id, attribute):
    """
    Remove attributes from a user
    ---
    """
    global url
    ngac = NGAC(token=request.headers["token"], policy_server_url=url)
    attr = UserAttribute(attribute)
    user = User([attr], id=user_id)
    global current_policy

    status = ngac.remove_assignment(user, attr, target_policy=current_policy)
    return status.match(
        ok=lambda x: "Attribute unassigned",
        error=lambda x: ("Error", 400)
    )
