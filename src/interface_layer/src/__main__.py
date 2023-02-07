# Import external tools
from logging.handlers import RotatingFileHandler
from logging import Formatter, DEBUG
from flask import Flask, request
from json import loads
from configparser import ConfigParser as CP
import logging
from json import dumps
from requests import post, Response
# Import local tools
from NgacApi.ngac import NGAC
from result import Result, Ok, Error, unwrap, is_error
from NgacApi import *
from NgacApi.access_request import AccessRequest
from NgacApi.user import User
from NgacApi.resource import Resource
from NgacApi.policy import Policy
from NgacApi.parser import parse, get_user_attributes, get_objects_attributes
from result import to_error, Error
from require import fields, response
from NgacApi.attribute import ObjectAttribute

# Import local files
from admin.admin import *
from admin.admin import set_current_policy
from admin.admin import current_policy as ngac_pol


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


# Setup ABE
abe_url = cfg["ABE"]["url"]
encrypt = "/encrypt_file"
decrypt = "/decrypt_file"
create_file = "/make_file"
remove_file = "/delete_file"
def abe(endpoint: str): return f"{abe_url}{endpoint}"
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


def ok(response: Response) -> Result:
    if response.status_code < 200 or response.status_code >= 300:
        return Error(f"Server responded with {response.status_code}")

    return Ok(response.text)


def access(user_id, resource_id, access_mode) -> Result:
    """
    Checks if a user has access to a resource.
    """
    user = User([], id=user_id)
    resource = Resource([], id=resource_id)
    access_request: AccessRequest = (user, access_mode, resource)
    ret = ngac.validate(access_request).match(
        ok=lambda x: Ok(x) if x else Error("Access denied"),
        error=lambda x: Error("NGAC server error"),
    )
    return ret


@app.route("/read", methods=["POST"])
@fields(request)
def read(user_id, resource_id):
    """
    Reads a file from the server if the user has access to it.
    """
    def read_interal():

        result = ngac.read(Policy(name=current_policy))
        if is_error(result):
            return "There is no access policy loaded", 400
        pol = unwrap(result).split("\n")
        print(pol)
        attributes = get_user_attributes(user_id, pol)
        print(pol)
        print(attributes)
        if not attributes:
            attributes = []
        fields = dumps({
            "user_id": user_id,
            "attributes": attributes,
            "file_name": resource_id,
        })
        response = ok(post(abe(decrypt), data=fields))
        return response.match(
            ok=lambda x: (x, 200),
            error=lambda x: ("Decryption Error", 400)
        )
    res = access(user_id=user_id, resource_id=resource_id, access_mode="r")
    return res.match(
        ok=lambda x: read_interal(),
        error=lambda x: (x, 403)
    )


@app.route("/write", methods=["POST"])
@fields(request)
def write(user_id, resource_id, policy, content):
    """
    Writes a file to the server if the user has access to it.
    """
    logger.debug(f"{user_id} is trying to write to {resource_id}")

    result = access(user_id=user_id, resource_id=resource_id, access_mode="w")
    if is_error(result):
        return response(result.value, code=403)

    data = dumps(
        {
            "user_id": user_id,
            "file_name": resource_id,
            "policy": policy,
            "content": content
        }
    )
    return ok(post(abe(encrypt), data=data)).match(
        ok=lambda x: ("Success", 200),
        error=lambda x: (f"Error : {x}", 400)
    )


@app.route("/make_file", methods=["POST"])
@fields(request)
def make_file(user_id, resource_id, policy, object_attributes):
    logger.debug(f"{user_id} is trying to make a file with id {resource_id}")
    f = Resource(object_attributes, id=resource_id)
    status = ngac.add(f, current_policy)
    if is_error(status):
        logger.error(
            "User tried to create a file that it does not have access to")
        print(status.value)
        return "Could not create the file", 400

    data = dumps({
        "user_id": user_id,
        "file_name": resource_id,
    })

    return ok(post(abe(create_file), data=data)).match(
        ok=lambda _: "Created file successfully",
        error=lambda x: (f"Error when creating file: {x}", 400)

    )


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

    result = ngac.read(Policy(name=current_policy))
    if is_error(result):
        return "There is no access policy loaded", 400
    pol = unwrap(result).split("\n")
    attributes = get_objects_attributes(resource_id, pol)
    if not attributes:
        attributes = []

    f: Resource = Resource(
        # Cast all the string representations to object level attributes
        [ObjectAttribute(oa) for oa in attributes],
        id=resource_id,
    )
    res: Result = access(
        user_id=user_id, resource_id=resource_id, access_mode="w")
    if is_error(res):
        return response(res.value, code=403)

    status = ngac.remove(f, target_policy=current_policy)
    # Now remove the file from the target storage

    def remove_file_internal():
        data = dumps({
            "user_id": user_id,
            "file_name": resource_id,
        })
        return ok(post(abe(remove_file), data=data)).match(
            ok=lambda x: "file removed",
            error=lambda x: (f"Error : {x}", 400)
        )

    return status.match(
        ok=lambda _: remove_file_internal(), error=lambda x: (str(x), 403)
    )


if __name__ == "__main__":

    logger.info("Starting server")
    app.run()
    logger.info("Server started")
