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
# See API endponit.py for more info
from endpoint import *

PolicyAccessAPI: Endpoint = endpoint(
    "PolicyAccessAPI", "/paapi", derived_from=Endpoint)
"""
Policy access API
---

This is the endpoint that you talk to when you want to modify the NGAC server.
"""
PolicyQueryAPI: Endpoint = endpoint(
    "PolicyQueryAPI", "/pqapi", derived_from=Endpoint)
"""
Policy Query Api
---

This is the endpoint that you talk to when you want to check if a certain thing is 
valid, such as access requests.
"""

EnforcementPoint: Endpoint = endpoint(
    "EnforcementPoint", "/epp", derived_from=Endpoint)
"""
EnforcementPoint
---

The endpoint that is used to change the context and similar of the enforcement point
"""


#############################################################################
#                              Paapi endpoints                              #
#############################################################################

LoadPolicy: Endpoint = endpoint(
    "LoadPolicy", "/loadpol", derived_from=PolicyAccessAPI)
SetPolicy: Endpoint = endpoint(
    "SetPolicy", "/setpol", derived_from=PolicyAccessAPI)
GetPolicy: Endpoint = endpoint(
    "GetPolicy", "/getpol", derived_from=PolicyAccessAPI)
ReadPolicy: Endpoint = endpoint(
    "ReadPolicy", "/readpol", derived_from=PolicyAccessAPI)
"""
Endpoint to read the policy spec from the server
"""
CombinePolicy: Endpoint = endpoint("CombinePolicy", "/combinepol",
                                   derived_from=PolicyAccessAPI)
Add: Endpoint = endpoint("Add", "/add", derived_from=PolicyAccessAPI)
AddMultiple: Endpoint = endpoint(
    "AddMultiple", "/addm", derived_from=PolicyAccessAPI)
Delete: Endpoint = endpoint("Delete", "/delete", derived_from=PolicyAccessAPI)
DeleteMultiple: Endpoint = endpoint("DeleteMultiple", "/deletem",
                                    derived_from=PolicyAccessAPI)
PurgePolicy: Endpoint = endpoint("PurgePolicy", "/purgepol",
                                 derived_from=PolicyAccessAPI)
InnitSession: Endpoint = endpoint("InnitSession", "/initsession",
                                  derived_from=PolicyAccessAPI)
EndSession: Endpoint = endpoint("EndSession", "/endsession",
                                derived_from=PolicyAccessAPI)
"""
https://github.com/ivario123/tog-ngac-crosscpp/blob/master/TEST/02-serverCombinedtest.sh#L27
"""
LoadImmediate: Endpoint = endpoint("LoadImmediate", "/loadi",
                                   derived_from=PolicyAccessAPI)
"""
See line 2-14 in 03-loaditest2.sh
"""

#############################################################################
#                              Pqapi endpoints                              #
#############################################################################
Access: Endpoint = endpoint("Access", "/access", derived_from=PolicyQueryAPI)


#############################################################################
#                                EPP endpoints                              #
#############################################################################
ContextNotify: Endpoint = endpoint(
    "ContextNotify", "/context_notify", derived_from=EnforcementPoint
)
