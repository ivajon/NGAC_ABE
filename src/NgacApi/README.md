# Next Generation Access Control (NGAC)

This folder contains the source code for the python wrapper for the Next Generation Access Control (NGAC) system. The [system itself](./tog-ngac-croscpp) is written in prolog and can be compiled into executables. The python wrapper is used to interface with the system.

## Repository Structure

```sh
|- ngac_types/                # NGAC types
|- executables/               # NGAC executables
| access_request.py           # Access Request class
| api.py                      # NGAC endpoints
| ngac.py                     # NGAC python frontend
| info.py                     # NGAC info
```

## NGAC Types

- [Policy](./ngac_types/ngac_policy.py)
- [User](./ngac_types/user.py)
- [Resource](./ngac_types/resource.py)
- [ngac_object](./ngac_types/ngac_object.py)
- [Attribute](./ngac_types/attribute.py)
- [UserAttribute](./ngac_types/attribute.py)
- [ResourceAttribute](./ngac_types/attribute.py)

## Starting the NGAC system

```sh
# Run the executable
cd executables
./better_start_ngac.sh
```

## Interfacing with the NGAC system using python

```python
from ngac import NGAC
from ngac_types.ngac_policy import Policy

# Create the ngac API class
ngac = NGAC()

# Create a policy, we will load from a file on disk
pol = Policy(
        name="Vehicle Ownership Policy", path="EXAMPLES/policy_vehicle_ownership.pl"
)

# Switch to the policy
ngac.switch_to(pol,token = "admin_token")

# Ensure the policy is loaded
print(ngac.get(Policy,token = "admin_token"))
```
