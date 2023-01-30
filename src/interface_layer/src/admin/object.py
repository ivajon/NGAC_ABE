"""
This module should require the admin role, but we
don't handle authentication yet.
"""
from flask import Blueprint, request

from result import *
from require import fields, response
from NgacApi.attribute import ObjectAttribute
from NgacApi.ngac import NGAC
from NgacApi.resource import Resource


resource = Blueprint("resource", __name__, url_prefix="/resource")


@resource.route("/new", methods=["POST"])
@fields(request)
def make_resource(object_id, attribute):
    """
    Creates a new resource
    ---
    """
    ngac = NGAC(token=request.headers["token"])
    object = Resource([ObjectAttribute(attribute)], id=object_id)
    return ngac.add_resource(object).match(
        lambda x: response("Resource created"),
        lambda x: response(f"Error {x.value}", code=400)
    )


@resource.route("assign", methods=["POST"])
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


@resource.route("unassign", methods=["POST"])
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
