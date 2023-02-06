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
from configparser import ConfigParser
from . import url


resource = Blueprint("resource", __name__, url_prefix="/resource")


@resource.route("/new", methods=["POST"])
@fields(request)
def make_resource(object_id, attribute):
    """
    Creates a new resource
    ---
    """
    global url
    ngac = NGAC(token=request.headers["token"], policy_server_url=url)
    object = Resource([ObjectAttribute(attribute)], id=object_id)
    return ngac.add_resource(object).match(
        lambda x: ("Resource created"),
        lambda x: (f"Error {x.value}", 400)
    )


@resource.route("/assign", methods=["POST"])
@fields(request)
def object_assign(object_id, attribute):
    """
    Assign attributes to a resource
    ---
    """
    global url
    ngac = NGAC(token=request.headers["token"], policy_server_url=url)
    attr = ObjectAttribute(attribute)
    object = Resource([attr], id=object_id)

    return ngac.assign(object, attr).match(
        lambda x: ("Attribute assigned"),
        lambda x: (f"Error {x.value}", 400)
    )


@resource.route("/unassign", methods=["POST"])
@fields(request)
def object_unassign(object_id, attribute):
    """
    Remove attributes from a resource
    ---
    """
    global url
    ngac = NGAC(token=request.headers["token"], policy_server_url=url)
    attr = ObjectAttribute(attribute)
    object = Resource([attr], id=object_id)

    return ngac.remove_assignment(object, attr).match(
        lambda x: ("Attribute unassigned"),
        lambda x: (f"Error {x.value}", 400)
    )
