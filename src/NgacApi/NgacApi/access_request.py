"""
Access Request
---

A type level abstraction of an access request.
"""

from typing import Tuple
import os

from .user import *
from .resource import *

# Define a tuple type, (user,operation,resource)
AccessRequest = Tuple[User, str, Resource]
"""
Access Request
---

Access request abstraction, this is used to verify an access request.

Access requests could be something like `Bob wants to read X.txt` This would be described
```python
bob = User(attributes = [], id = "Bob")
x = Resource(attributes = [], id = "X.txt")

ar = AccessRequest(Bob,"r",x)
```
"""


def test_access_request():
    """
    Test access request
    """
    u1 = User("user")
    r1 = Resource("resource")
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
