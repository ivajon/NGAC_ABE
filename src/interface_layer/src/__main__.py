# Import external tools
from logging.handlers import RotatingFileHandler
from logging import Formatter, DEBUG
from flask import Flask, request
from json import loads
from configparser import ConfigParser as CP
import logging
from json import dumps, loads
from requests import post, Response

# Import local tools
from NgacApi import NGAC, AccessRequest, User, Resource, Policy, ObjectAttribute
from result import Result, Ok, Error, unwrap, is_error
from NgacApi.parser import (
    get_user_attributes,
    get_objects_attributes,
    get_connection,
    parse,
)
from result import to_error, Error
from require import fields, response

# Import local files
from admin.admin import *
from admin import set_current_policy, get_policy


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
ngac = NGAC(token=admin_token, policy_server_url=cfg["ABE"]["url"])
# ------------------------------


# Setup ABE
ABE_URL = cfg["ABE"]["url"]
ENCRYPT = "/encrypt_file"
DECRYPT = "/decrypt_file"
RESET = "/reset_files"
CREATE_FILE = "/make_file"
REMOVE_FILE = "/delete_file"


def abe(endpoint: str):
    return f"{ABE_URL}{endpoint}"


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
set_current_policy(policy_name)
# ------------------------------


def ok(response: Response) -> Result:

    logger.error(response.text)
    if response.status_code < 200 or response.status_code >= 300:
        return Error(f"Server responded with {response.status_code}")

    return Ok(loads(response.text)["content"])


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


@app.route("/reset_database", methods=["POST"])
def reset_database():
    response = post(abe(RESET), data=None)
    return (
        "RESET"
        if response.status_code == 200
        else ("Error when resetting the database", 400)
    )


@app.route("/read", methods=["POST"])
@fields(request)
def read(user_id: str, resource_id: str):
    """
    Reads a file from the server if the user has access to it.
    """

    def read_interal():

        result = ngac.read(Policy(name=get_policy()))
        if is_error(result):
            return "There is no access policy loaded", 400
        pol = unwrap(result).split("\n")
        attributes = get_user_attributes(user_id, pol)
        conn: tuple[str, str] = get_connection(user_id, resource_id, "r", pol)
        if not attributes:
            attributes = []
        fields = dumps(
            {
                "user_id": user_id,
                "attributes": attributes,
                "policy": f'("{conn[1]}")',
                "file_name": resource_id,
            }
        )
        print(f"{abe(DECRYPT)} post {fields=}")
        response = ok(post(abe(DECRYPT), data=fields))
        return response.match(
            ok=lambda x: (x, 200), error=lambda x: ("Decryption Error", 400)
        )

    res = access(user_id=user_id, resource_id=resource_id, access_mode="r")
    return res.match(ok=lambda x: read_interal(), error=lambda x: (x, 403))


@app.route("/write", methods=["POST"])
@fields(request)
def write(user_id: str, resource_id: str, content: str):
    """
    Writes a file to the server if the user has access to it.
    """
    logger.debug(f"{user_id} is trying to write to {resource_id}")

    result = access(user_id=user_id, resource_id=resource_id, access_mode="w")
    if is_error(result):
        return response(result.value, code=403)
    pol = ngac.read(Policy(name=get_policy()))
    if is_error(pol):
        return "Error when reading the policy from server", 400
    pol = unwrap(pol).split("\n")

    conn: tuple[str, str] = get_connection(user_id, resource_id, "w", pol)

    # We know that there is some connection since the user
    # has access to that resource
    policy = f'("{conn[0]}")'
    logger.info(
        f"Found shortest access policy of {policy} since there exists a write association {conn}"
    )
    obj_attr = get_objects_attributes(resource_id, pol)
    data = dumps(
        {
            "user_id": user_id,
            "file_name": resource_id,
            "content": content,
            "attributes": obj_attr,
            "policy": policy,
        }
    )
    ret = post(abe(ENCRYPT), data=data)
    print(f"{abe(ENCRYPT)} post {data=} => {ret.text=}")
    return ("Success", 200) if ret.status_code == 200 else (f"Error when writing", 400)


@app.route("/make_file", methods=["POST"])
@fields(request)
def make_file(user_id: str, resource_id: str, object_attributes: list):
    logger.debug(f"{user_id} is trying to make a file with id {resource_id}")
    pol = Policy(name=get_policy())
    logger.info(f"{pol=}")
    text_repr = unwrap(ngac.read(pol)).split("\n")
    logger.info(f"{text_repr=}")
    parsed = parse(text_repr)
    logger.info(f"{parsed=}")
    if resource_id in parsed["object"].keys():
        return "File already exists", 400
    f = Resource(object_attributes, id=resource_id)
    status = ngac.add(f, get_policy())
    if is_error(status):
        logger.error("User tried to create a file that it does not have access to")
        print(status.value)
        return "Could not create the file", 400
    return "Created file successfully"


@app.route("/delete_file", methods=["POST"])
@fields(request)
def delete_file(user_id: str, resource_id: str):
    """
    Removes a file from the server
    ---

    Note: This will not remove the attributes from the policy,
    it will remove the object and the assigned attributes from the policy.
    """
    logger.debug(f"{user_id} is trying to delete a file with id {resource_id}")

    result = ngac.read(Policy(name=get_policy()))
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
    res: Result = access(user_id=user_id, resource_id=resource_id, access_mode="w")
    if is_error(res):
        return response(res.value, code=403)

    status = ngac.remove(f, target_policy=get_policy())
    # Now remove the file from the target storage

    def remove_file_internal():
        data = dumps(
            {
                "user_id": user_id,
                "file_name": resource_id,
            }
        )
        return ok(post(abe(REMOVE_FILE), data=data)).match(
            ok=lambda x: "file removed", error=lambda x: (f"Error : {x}", 400)
        )

    return status.match(
        ok=lambda _: remove_file_internal(), error=lambda x: (str(x), 403)
    )


if __name__ == "__main__":

    logger.info("Starting server")
    app.run()
    logger.info("Server stopped")
