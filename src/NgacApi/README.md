# Next Generation Access Control (NGAC)

This folder contains the source code for the python wrapper for the Next Generation Access Control (NGAC) system. The python wrapper is used to interface with the system.

## Repository Structure

```sh
|- NgacApi/                   # NGAC API source code (installed as a package)
|  |- __init__.py             # Init file
|  |- access_request.py       # Access request class
|  |- attribute.py            # Attribute class ( resource and user attributes )
|  |- endpoints.py            # Defines the endpoints for the API ( type level abstraction )
|  |- errors.py               # Defines the errors for the API
|  |- info.py                 # Defines some coloring and formatting for the API terminal output
|  |- ngac_object.py          # Defines the base class for all NGAC objects ( all inherit from this )
|  |- ngac.py                 # Defines the NGAC class ( the main class for the API )
|  |- parser.py               # Defines the parser class ( used to parse ngac policies to python objects )
|  |- policy_element.py       # Defines the policy element class ( used to represent policy elements )
|  |- policy.py               # Defines the policy class ( used to represent policies )
|  |- resource.py             # Defines the resource class ( used to represent resources )
|  |- user.py                 # Defines the user class ( used to represent users )
|  |- test.py                 # Defines some tests for the API
```

## NGAC Types

- [Policy](./ngac_types/ngac_policy.py)
- [User](./ngac_types/user.py)
- [Resource](./ngac_types/resource.py)
- [ngac_object](./ngac_types/ngac_object.py)
- [Attribute](./ngac_types/attribute.py)
- [UserAttribute](./ngac_types/attribute.py)
- [ResourceAttribute](./ngac_types/attribute.py)

