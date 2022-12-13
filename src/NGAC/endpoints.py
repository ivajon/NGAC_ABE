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

EnforcementPoint = endpoint("EnforcementPoint", "/epp", derived_from=Endpoint)
"""
EnforcementPoint
---

The endpoint that is used to change the context and similar of the enforcement point
"""


#############################################################################
#                              Paapi endpoints                              #
#############################################################################

LoadPolicy = endpoint("LoadPolicy", "/loadpol", derived_from=PolicyAccessAPI)
SetPolicy = endpoint("SetPolicy", "/setpol", derived_from=PolicyAccessAPI)
GetPolicy = endpoint("GetPolicy", "/getpol", derived_from=PolicyAccessAPI)
ReadPolicy = endpoint("ReadPolicy", "/readpol", derived_from=PolicyAccessAPI)
"""
Endpoint to read the policy spec from the server
"""
CombinePolicy = endpoint("CombinePolicy", "/combinepol", derived_from=PolicyAccessAPI)
Add = endpoint("Add", "/add", derived_from=PolicyAccessAPI)
AddMultiple = endpoint("AddMultiple", "/addm", derived_from=PolicyAccessAPI)
Delete = endpoint("Delete", "/delete", derived_from=PolicyAccessAPI)
DeleteMultiple = endpoint("DeleteMultiple", "/deletem", derived_from=PolicyAccessAPI)
PurgePolicy = endpoint("PurgePolicy", "/purgepol", derived_from=PolicyAccessAPI)
InnitSession = endpoint("InnitSession", "/initsession", derived_from=PolicyAccessAPI)
EndSession = endpoint("EndSession", "/endsession", derived_from=PolicyAccessAPI)
"""
https://github.com/ivario123/tog-ngac-crosscpp/blob/master/TEST/02-serverCombinedtest.sh#L27
"""
LoadImmediate = endpoint("LoadImmediate", "/loadi", derived_from=PolicyAccessAPI)
"""
See line 2-14 in 03-loaditest2.sh
"""

#############################################################################
#                              Pqapi endpoints                              #
#############################################################################
Access = endpoint("Access", "/access", derived_from=PolicyQueryAPI)



#############################################################################
#                                epp endpoints                              #
#############################################################################
ContextNotify = endpoint("ContextNotify","/context_notify",derived_from=EnforcementPoint)

