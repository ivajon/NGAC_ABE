"""
Errors
---

Defines a set of possible errors for the NGAC api
"""

from result import *


def http_error(status: int):
    """
    Creates a new HTTP error
    """
    return to_error(f"HttpError{status}", "An HTTP error occurred")


def generic_NGAC_error(text: str):
    """
    Creates a new NGAC error
    """
    return to_error(f"GenericNGACError", text)


NoServerResponse = to_error(
    "NoServerResponse", "The server did not respond to a request"
)
"""
The server did not respond to a request
"""

NoSuchPolicy = to_error("NoSuchPolicy", "The policy does not exist")
"""
The policy does not exist
"""

action_error = to_error("ActionError", "The action was not valid")
