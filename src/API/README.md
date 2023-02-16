# API

- `Endpoint`: A type-level abstraction for building APIs.

## Endpoint

An `Endpoint` is a type-level abstraction for building APIs. It is a type that helps
you build a type-safe ( type-safer ) API in python.

### Example

```python
from endpoint import *

PolicyAccessAPI: Endpoint = endpoint(
    "PolicyAccessAPI", "/paapi", derived_from=Endpoint)
"""
Policy access API
---
This is the policy endpoint
"""

LoadPolicy: Endpoint = endpoint(
    "LoadPolicy", "/loadpol", derived_from=PolicyAccessAPI)


def load_policy(policy_id: str) -> str:
    """
    Load a policy
    ---
    Loads a policy from the database
    """

    # Renders the url as: some.url/paapi/loadpol
    url = f"some.url/{LoadPolicy()}"
    data = {"policy_id": policy_id}
    response = requests.post(url, data=data)
    return response.json()

```
