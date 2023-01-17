"""
Endpoint
---

A type level abstraction for an endpoint. This is used to create new endpoints
for the API.

## Usage

```python
from API import endpoint, Endpoint

MyEndpoint = endpoint("MyEndpoint",
                      "/myendpoint",
                      derived_from=Endpoint)

def call_endpoint(endpoint: Endpoint):
    # Call to that endpoint, now we know that it is a valid endpoint
    pass
```
"""


class Endpoint:
    """
    Endpoint
    ---

    An API endpoint abstraction. Calling str() on an Endpoint will return the endpoint as a string.
    """

    def __str__(self) -> str:
        """
        Returns the endpoint as a string
        """
        return ""

    def __repr__(self) -> str:
        """
        Returns the endpoint as a string
        """
        return self.__str__()


def endpoint(name, endpoint, derived_from):
    """
    Creates a new `endpoint`
    ---

    Resulting format of the endpoint is
    ```
    f"/{str(derived_from)}/{endpoint}"
    ```
    """

    return type(
        name,
        (derived_from,),
        {
            "__repr__": lambda self: str(derived_from()) + endpoint,
            "__str__": lambda self: self.__repr__(),
            "name": name,
        },
    )
