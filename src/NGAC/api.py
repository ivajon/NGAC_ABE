"""
Defines an API for the NGAC system.


"""

POLICY_ACCESS_ENDPOINT = "paapi"
"""
Policy access API,
This is used to set, get and manipulate policies

## Example
```bash
curl -s -G "http://127.0.0.1:8001/paapi/loadpol" --data-urlencode "policyfile=EXAMPLES/policy_signals_access.pl" --data-urlencode "token=admin_token"
```
"""

POLICY_QUERY_ENDPOINT = "pqapi"
"""
Policy query API,
This is used to query the policy server for information

## Example
```bash
curl -s -G "http://127.0.0.1:8001/pqapi/access" --data-urlencode "user=jones" --data-urlencode "ar=read" --data-urlencode "object=mrec1"
```
"""


POLICY_LOAD_ENDPOINT = "loadpol"

"""API = {
    POLICY_ACCESS_ENDPOINT: {
        "load": "loadpol",
        "set": "setpol",
        "get": "getpol",
        "combine": "combinepol",
        "add": "add",
        "delete": "delete",
        "purge": "purgepol",
    },
    POLICY_QUERY_ENDPOINT: {
        "access": "access",
    },
}"""
"""
API definition for the NGAC server

This is very implementation specific, and will need to be changed
if the NGAC server is changed.
"""


class Operation:
    """
    Defines an operation for the API
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


def operation(name, endpoint, derived_from):
    """
    Creates a new operation class
    """

    return type(
        name,
        (derived_from,),
        {
            "__repr__": lambda self: str(derived_from()) + endpoint,
            "__str__": lambda self: self.__repr__(),
        },
    )


PolicyAccessAPI = operation("PolicyAccessAPI", "/paapi", derived_from=Operation)
PolicyQueryAPI = operation("PolicyQueryAPI", "/pqapi", derived_from=Operation)

LoadPolicy = operation("LoadPolicy", "/loadpol", derived_from=PolicyAccessAPI)
SetPolicy = operation("SetPolicy", "/setpol", derived_from=PolicyAccessAPI)
GetPolicy = operation("GetPolicy", "/getpol", derived_from=PolicyAccessAPI)
CombinePolicy = operation("CombinePolicy", "/combinepol", derived_from=PolicyAccessAPI)
AddPolicy = operation("AddPolicy", "/add", derived_from=PolicyAccessAPI)
DeletePolicy = operation("DeletePolicy", "/delete", derived_from=PolicyAccessAPI)
PurgePolicy = operation("PurgePolicy", "/purgepol", derived_from=PolicyAccessAPI)

Access = operation("Access", "/access", derived_from=PolicyQueryAPI)


class API:
    def __init__(self, operations):
        self.operations = operations

    def __str__(self):
        repr = "API:\n"
        for operation in self.operations:
            repr += f"\t{type(operation).__name__}: {operation}\n"
        return repr


def test_api():
    api = API(
        [
            LoadPolicy(),
            SetPolicy(),
            GetPolicy(),
            CombinePolicy(),
            AddPolicy(),
            DeletePolicy(),
            PurgePolicy(),
            Access(),
        ]
    )
    print(api)


if __name__ == "__main__":
    test_api()
