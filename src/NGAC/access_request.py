"""
Represents an access request to the PDP.
"""

from typing import Tuple
import os

if os.getcwd().endswith("src"):
    from NGAC.ngac_types import user, resource, ngac_policy
else:
    from ngac_types import user, resource, ngac_policy

# Define a tuple type, (user,operation,resource)
AccessRequest = Tuple[user.User, str, resource.Resource]


def test_access_request():
    """
    Test access request
    """
    if os.getcwd().endswith("src"):
        from NGAC.ngac_types import user, resource, ngac_policy
    else:
        from ngac_types import user, resource, ngac_policy

    u1 = user.User("user")
    r1 = resource.Resource("resource")
    operation = "Read"
    access_request = (u1, operation, r1)

    def validate_access_request(access_request: AccessRequest):
        """
        Validates an access request
        """
        assert isinstance(access_request[0], user.User)
        assert isinstance(access_request[1], str)
        assert isinstance(access_request[2], resource.Resource)

    validate_access_request(access_request)
