"""
API
---

Defines all of the valid endpoints for the NGAC API

## Endpoints

## Policy Access API
- LoadPolicy
- SetPolicy
- GetPolicy
- CombinePolicy
- AddPolicy
- DeletePolicy
- PurgePolicy
## Policy Query API
- Access
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


PolicyAccessAPI = endpoint("PolicyAccessAPI", "/paapi", derived_from=Endpoint)
"""
Policy access API
---

This is the endpoint that you talk to when you want to modify the NGAC server.
"""
PolicyQueryAPI = endpoint("PolicyQueryAPI", "/pqapi", derived_from=Endpoint)
"""
Policy Query Api
---

This is the endpoint that you talk to when you want to check if a certain thing is 
valid, such as access requests.
"""

LoadPolicy = endpoint("LoadPolicy", "/loadpol", derived_from=PolicyAccessAPI)
SetPolicy = endpoint("SetPolicy", "/setpol", derived_from=PolicyAccessAPI)
GetPolicy = endpoint("GetPolicy", "/getpol", derived_from=PolicyAccessAPI)
CombinePolicy = endpoint("CombinePolicy", "/combinepol", derived_from=PolicyAccessAPI)
AddPolicy = endpoint("AddPolicy", "/add", derived_from=PolicyAccessAPI)
DeletePolicy = endpoint("DeletePolicy", "/delete", derived_from=PolicyAccessAPI)
PurgePolicy = endpoint("PurgePolicy", "/purgepol", derived_from=PolicyAccessAPI)

Access = endpoint("Access", "/access", derived_from=PolicyQueryAPI)
