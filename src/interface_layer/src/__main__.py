# Import external tools
from logging.handlers import RotatingFileHandler
from logging import basicConfig, Formatter, DEBUG
from flask import Flask, request
from json import loads
from configparser import ConfigParser as CP
import logging
from typing import Tuple
from require import fields, response
# Import local tools
from NgacApi.ngac import NGAC
from result import Result, Ok, Error, unwrap, is_error
from NgacApi import *
from NgacApi.access_request import AccessRequest
from NgacApi.user import User
from NgacApi.resource import Resource
from NgacApi.policy import Policy
from result import to_error, Error

# Import local files
from admin.admin import *
from admin.admin import set_current_policy


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
logger.setLevel(DEBUG)  # cfg["logging"]["level"])
# ------------------------------


# Set up the flask app
app = Flask(__name__)
app.register_blueprint(admin)
# ------------------------------


# Set up the NGAC
with open(cfg["NGAC"]["admin_token"], "r") as f:
    admin_token = f.read()
ngac = NGAC(token=admin_token, policy_server_url="http://130.240.200.92:8001")
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
pol = Policy(name=policy_name)
print(ngac.read(pol))
set_current_policy(policy_name)
# ------------------------------


def access(user_id, resource_id, access_mode) -> Result:
    """
    Checks if a user has access to a resource
    """
    user = User([], id=user_id)
    resource = Resource([], id=resource_id)
    access_request: AccessRequest = (user, access_mode, resource)
    print(access_request)
    ret = ngac.validate(access_request).match(
        ok=lambda x: Ok(x) if x else Error("Access denied"),
        error=lambda x: Error("NGAC server error"),
    )
    return ret


@app.route("/read", methods=["POST"])
@fields(request)
def read(user_id, resource_id):
    def read_interal():
        print("This should be replaced by a decrypt call")
        return response("This is the file", code=200)
    print(f"{user_id} is trying to read {resource_id}")
    res = access(user_id=user_id, resource_id=resource_id, access_mode="r")
    print(res)
    return res.match(
        ok=lambda x: read_interal(),
        error=lambda x: (x, 403)
    )


@app.route("/write", methods=["POST"])
@fields(request)
def write(user_id, resource_id, policy):
    logger.debug(f"{user_id} is trying to write to {resource_id}")

    result = access(user_id=user_id, resource_id=resource_id, access_mode="w")
    if is_error(result):
        return response(result.value, code=403)

    return "Time for ABE magic"


@app.route("/make_file", methods=["POST"])
@fields(request)
def make_file(user_id, resource_id, policy, object_attributes):
    # Now parse the request data
    logger.debug(f"{user_id} is trying to make a file with id {resource_id}")
    f = Resource(object_attributes, id=resource_id)
    status = ngac.add(f, current_policy)
    ret = status.match(ok=lambda x: response("File was created"),
                       error=lambda x: response(f"Could not create file: {x}", 400))
    # Do some black magic to make the file on server
    return ret


@app.route("/delete_file", methods=["POST"])
@fields(request)
def delete_file(user_id, resource_id):
    """
    Removes a file from the server
    ---

    Note: This will not remove the attributes from the policy,
    it will remove the object and the assigned attributes from the policy.
    """
    logger.debug(f"{user_id} is trying to delete a file with id {resource_id}")
    # This should not be needed, placeholder for parsing the attributes of the file
    data = loads(request.data)
    f: Resource = Resource(
        [] if not "object_attributes" in data.keys() else data["object_attributes"],
        id=resource_id,
    )
    u: User = User([], id=user_id)
    res: Result = access(
        user_id=user_id, resource_id=resource_id, access_mode="w")
    if is_error(res):
        return response(res.value, code=403)

    status = ngac.remove(f, target_policy=current_policy)
    # Now remove the file from the target storage
    return status.match(
        ok=lambda _: ("delete_file", 200), error=lambda x: (str(x), 403)
    )


if __name__ == "__main__":

    logger.info("Starting server")
    app.run()
    logger.info("Server started")
