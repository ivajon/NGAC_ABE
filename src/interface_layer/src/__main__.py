# Import external tools
from logging.handlers import RotatingFileHandler
from logging import basicConfig, Formatter
from flask import Flask, request
from json import loads
from configparser import ConfigParser as CP
import logging

# Import local tools
from NgacApi.ngac import NGAC
from API.result import Result, Ok, Error, unwrap, is_error
from NgacApi import *
from NgacApi.access_request import AccessRequest
from NgacApi.user import User
from NgacApi.resource import Resource
from NgacApi.policy import Policy
from API.result import to_error, Error

# Import local files
from .admin.admin import *


# Set up logging
logger = logging.getLogger(__name__)
cfg = CP()
# ------------------------------


# Load the config file
files_read = cfg.read("data/SERVER.ini")
if len(files_read) == 0:
    raise FileNotFoundError("Could not find data/SERVER.ini")
# ------------------------------

# Initiate the logger
file_handler = RotatingFileHandler(
    cfg["logging"]["folder"] + "/server.log",
    maxBytes=int(cfg["logging"]["maxBytes"]),
)
file_handler.setLevel(cfg["logging"]["level"])
file_handler.setFormatter(
    Formatter("%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s")
)
logger.addHandler(file_handler)
logger.setLevel(cfg["logging"]["level"])
# ------------------------------


# Set up the flask app
app = Flask(__name__)
# ------------------------------


# Set up the NGAC
with open(cfg["NGAC"]["admin_key"], "r") as f:
    admin_token = f.read()
ngac = NGAC(token=admin_token)
# ------------------------------


def error(value) -> Error:
    """
    Error
    ---
    Error modal, wraps the [`ErrorType`] class.
    """
    return to_error(value, value)


# Load the policy
pol = cfg["NGAC"]["policy"]
with open("data/" + pol, "r") as f:
    policy = f.read()

unwrap(ngac.load_policy_from_str(policy))
policy_name = pol.split(".")[0]
current_policy = Policy(name=policy_name)
logger.debug(f"Loading {current_policy.name}...")
unwrap(ngac.change_policy(current_policy))
logger.debug(f"Loaded the policy")
# ------------------------------


def has_keys(keys, dictionary):
    """
    Checks if a dictionary has all the keys in a list
    ---
    """
    for key in keys:
        if key not in dictionary.keys():
            return Error(key)
    return Ok("")


def access(args) -> Result:
    """
    Checks if a user has access to a resource
    """
    try:
        user = User([], id=args["user_id"])
        resource = Resource([], id=args["file_name"])
    except:
        return error("Invalid arguments")

    access_request: AccessRequest = (user, "r", resource)
    access = ngac.validate(access_request)
    if not access:
        return error("Access denied")
    return Ok((user, resource))


@app.route("/read", methods=["POST"])
def read():
    logger.debug("Read request, with data: " + str(request.data))
    data = loads(request.data)
    ret = has_keys(["user_id", "object_id"], data)
    if is_error():
        logger.debug("Invalid invalid arguments")
        return (
            str(
                f"Invalid arguments: {data}, expected: user_id, object_id. Atleast missing : {ret.value} in json format"

            ), 400,
        )
    result = access(data)
    return result.match(
        ok=lambda x: (f"{x[0]} has access to {x[1]}", 200),
        error=lambda x: (f"Access denied: {x}", 403),
    )


@app.route("/write", methods=["POST"])
def write():
    # Log the write request
    logger.debug("Write request, with data: " + str(request.data))
    data = loads(request.data)
    ret = has_keys(["user_id", "object_id", "policy"], data)
    if is_error(ret):
        logger.debug("Invalid invalid arguments")
        return (
            str(
                f"Invalid arguments: {data}, expected: user_id, object_id, policy. Atleast missing : {ret.value} in json format"
            ),
            400,
        )

    result = access(data)
    if is_error(result):
        return str(result.value), 403

    user_id = data["user_id"]
    file_name = data["object_id"]
    policy = data["policy"]
    return "Time for ABE magic"


@app.route("/make_file", methods=["POST"])
def make_file():
    # Now parse the request data
    logger.debug("Make file request, with data: " + str(request.data))
    data = loads(request.data)
    ret = has_keys(["user_id", "object_id", "policy",
                   "object_attributes"], data)
    if is_error(ret):
        logger.debug("Invalid invalid arguments")
        return (
            str(
                f"Invalid arguments: {data}, expected: user_id, object_id, policy. Atleast missing : {ret.value} in json format"
            ),
            400,
        )

    f = Resource(data["object_attributes"], id=data["object_id"])
    status = ngac.add(f, current_policy)
    ret = status.match(ok=lambda x: ("make_file", 200),
                       error=lambda x: (str(x), 400))
    # Do some black magic to make the file on server
    return ret


@app.route("/delete_file", methods=["POST"])
def delete_file():
    """
    Removes a file from the server
    ---

    Note: This will not remove the attributes from the policy,
    it will remove the object and the assigned attributes from the policy.
    """

    # Here we need to use the policy parser to get all the attributes for the file
    # We should not trust the user to know all object attributes

    # Now parse the request data
    data = loads(request.data)

    ret = has_keys(["user_id", "object_id"], data)
    if is_error(ret):
        return (
            f"Invalid arguments: {data}, expected: user_id, object_id. Atleast missing : {ret.value} in json format",
            400,
        )
    logger.debug(f"Delete request for file with data : {data} ")

    f: Resource = Resource(
        [] if "object_attributes" not in data.keys() else data["object_attributes"],
        id=data["object_id"],
    )
    access_request: AccessRequest = (User([], id=data["user_id"]), "w", f)

    def remove_file(f: Resource):
        status = ngac.remove(f, target_policy=current_policy)
        return status.match(
            ok=lambda _: ("delete_file", 200), error=lambda x: (str(x), 403)
        )

    return ngac.validate(access_request).match(
        ok=lambda x: remove_file(f) if x else ("Access denied", 403),
        error=lambda _: ("Internal server error, try again later", 400),
    )


if __name__ == "__main__":

    logger.info("Starting server")
    app.run()
    logger.info("Server started")
