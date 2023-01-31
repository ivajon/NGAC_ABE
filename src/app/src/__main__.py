from requests import post
from logging import DEBUG, ERROR, getLogger, StreamHandler
from __init__ import parser
import json
import sys

logger = getLogger(__name__)
logger.addHandler(StreamHandler(
    stream=sys.stdout
))
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
            "data": data,
        }
    )
    if response.status_code == 200:
        logger.debug("File written successfully.")
        print(f"File written successfully: {args.file}")
    else:
        logger.error("Error writing file: %s", response.text)
        error_logger.error("Error writing file: %s", response.text)
        exit(-1)


def handle_delete(args):
    logger.debug("Deleting file: %s", args.file)
    response = post(
        url("/delete_file", args),
        json={
            "user_id": "u1",
            "resource_id": "o1",
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


if __name__ == "__main__":
    args = parser.parse_args()
    if args.debug:
        logger.setLevel(DEBUG)

    # Get the value of the subcommand
    read = parser.parse_args(["read"])
    write = parser.parse_args(["write"])
    delete = parser.parse_args(["delete"])

    if args.command == "read":
        logger.debug("Read command")
        logger.debug("Reading file: %s", args.file)
        handle_read(args)
        exit()
    elif args.command == "write":
        logger.debug("Write command")
        handle_write(args)
        exit()
    elif args.command == "delete":
        logger.debug("Delete command")
        handle_delete(args)
        exit()
