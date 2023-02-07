import sys
from logging import DEBUG, ERROR, StreamHandler, getLogger
from requests import post
from __init__ import parser

logger = getLogger(__name__)
logger.addHandler(
    StreamHandler(
        stream=sys.stdout
    )
)
# Error logger, log to file
error_logger = getLogger("error")
error_logger.addHandler(StreamHandler(
    stream=open("error.log", "w+")
))
error_logger.setLevel(ERROR)


def url(path, args):
    if args.url:
        return f"http://{args.url}:{args.port}{path}"
    else:
        return f"http://localhost:5000{path}"


def handle_read(args):
    """
    Handles reading data from the server
    ---

    Se documentation for [`NgacApi::validate`,`CryptographyService`,`INTERFACE_LAYER::READ`]
    """
    logger.debug("Reading file: %s", args.file)
    response = post(
        url("/read", args),
        json={
            "user_id": args.username, "resource_id": args.file
        }
    )
    if response.status_code == 200:
        logger.debug("File read successfully.")
        print(response.text)
    else:
        logger.error("Error reading file: %s", response.text)
        error_logger.error("Error reading file: %s", response.text)
        exit(-1)


def handle_write(args):
    """
    Handles writing data to the server
    ---

    Se documentation for [`NgacApi::validate`,`CryptographyService`,`INTERFACE_LAYER::WRITE`]
    """
    logger.debug("Writing file: %s", args.file)
    # Assume file exists
    with open(args.input, "r") as f:
        data = f.read()
    response = post(
        url("/write", args),
        json={
            "user_id": args.username,
            "resource_id": args.file,
            "object_attributes": ["oa1"],
            "policy": "A & !B",
            "content": data,
        }
    )
    if response.status_code == 200:
        logger.debug("File written successfully.")
        print(f"File written successfully: {args.file}")
    else:
        logger.error("Error writing file: %s", response.text)
        error_logger.error("Error writing file: %s", response.text)
        exit(-1)


def listify(attr):
    if not isinstance(attr, list):
        attr = [attr]
    return attr


def handle_delete(args):
    logger.debug("Deleting file: %s", args.file)
    response = post(
        url("/delete_file", args),
        json={
            "user_id": args.username,
            "resource_id": args.file,
            "object_attributes": ["oa1"],
            "policy": "A & !B",
        }
    )
    if response.status_code == 200:
        logger.debug("File deleted successfully.")
        print(f"File deleted successfully: {args.file}")
    else:
        logger.error("Error deleting file: %s", response.text)
        error_logger.error("Error deleting file: %s", response.text)
        exit(-1)


def handle_create(args):
    logger.debug("Deleting file: %s", args.file)
    response = post(
        url("/make_file", args),
        json={
            "user_id": args.username,
            "resource_id": args.file,
            "object_attributes": listify(args.object_attributes),
            "policy": "A & !B",
        }
    )
    if response.status_code == 200:
        logger.debug("File created successfully.")
        print(f"File created successfully: {args.file}")
    else:
        logger.error("Error while creating file: %s", response.text)
        error_logger.error("Error while creating file: %s", response.text)
        exit(-1)


"""
        Admin routes
"""


def handle_assign(args):

    [path, json] = (
        "/admin/user/assign",
        {
            "user_id": args.user,
            "attribute": args.attribute
        }
    )if args.user else (
        "/admin/object/assign",
        {
            "object_id": args.object,
            "attribute": args.attribute
        }
    )
    response = post(
        url(path, args),
        json=json,
        headers={"token": args.token}
    )

    if response.status_code != 200:
        error_logger.error("Error when assigning attribute")
        logger.error(
            "Error when assigning attribute")
        exit(-1)
    print("Attribute assigned successfully")


def handle_remove_assign(args):
    [path, json] = (
        "/admin/user/unassign",
        {
            "user_id": args.user,
            "attribute": args.attribute
        }
    )if args.user else (
        "/admin/object/unassign",
        {
            "object_id": args.object,
            "attribute": args.attribute
        }
    )
    response = post(
        url(path, args),
        json=json,
        headers={"token": args.token}
    )

    if response.status_code != 200:
        error_logger.error("Error when removing attribute assignment")
        logger.error(
            "Error when removing attribute assignment")
        exit(-1)
    print("Remove attribute assignment successfully")


def handle_readpol(args):
    logger.debug("Reading policy from server")
    response = post(
        url("/admin/read_policy", args),
        headers={
            "token": args.token
        }
    )
    if response.status_code != 200:
        error_logger.error("Error while reading policy")
        logger.error("Error while reading policy")
        exit(-1)
    print(response.text)


def handle_loadi(args):
    logger.debug("Loading new policy from file: %s", args.input_file)
    with open(args.input_file, 'r') as f:
        pol = f.read()
    polname = args.input_file.split('.')[0].split("/")[-1]
    response = post(
        url("/admin/load_policy", args),
        json={
            "policy": pol,
            "policy_name": polname
        },
        headers={
            "token": args.token
        }
    )
    if response.status_code == 200:
        logger.debug("Loaded policy.")
        print(f"Loaded policy successfully: {polname}")
    else:
        logger.error("Error while loading policy: %s", args.input_file)
        error_logger.error("Error while loading policy: %s", args.input_file)
        exit(-1)


def handle_admin(args):
    logger.debug("Admin request to %s", args.admin_command)
    cmd = args.admin_command
    eval(f"handle_{cmd}(args)")
    exit(0)


if __name__ == "__main__":
    args = parser.parse_args()
    if args.debug:
        logger.setLevel(DEBUG)
    # This is bad practice but we know that all of the
    # Function names are defined, and if they are not
    # we will get an error that the function called
    # does not exist which is fine.
    eval(f"handle_{args.command}(args)")
    exit(0)
