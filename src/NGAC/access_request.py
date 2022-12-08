"""
Access Request
---

A type level abstraction of an access request.
"""

from typing import Tuple
import os

if os.getcwd().endswith("src"):
    from .ngac_types import user, resource
else:
    from ngac_types import user, resource

# Define a tuple type, (user,operation,resource)
AccessRequest = Tuple[user.User, str, resource.Resource]
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
    if os.getcwd().endswith("src"):
        from NGAC.ngac_types import user, resource
    else:
        from ngac_types import user, resource

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
