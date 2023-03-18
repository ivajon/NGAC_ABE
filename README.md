# Attribute-Based Encryption (ABE) enabled by Next Generation Access Control (NGAC)

[![Unit Tests](https://github.com/ivario123/NGAC_ABE/actions/workflows/unit_tests.yml/badge.svg?branch=ngac_boilerplate)](https://github.com/ivario123/NGAC_ABE/actions/workflows/unit_tests.yml) [![SpellCheck](https://github.com/ivario123/NGAC_ABE/actions/workflows/spellcheck.yml/badge.svg?branch=ngac_boilerplate)](https://github.com/ivario123/NGAC_ABE/actions/workflows/spellcheck.yml) 

Here we should have some good filler text.

## Setup

Read the docs [readme](/docs/README.md)

## Prelude

Using third-party cloud servers may entail a risk as the owner no longer have control over the data. Therefore it's essential to ensure that only the trusted parties can read messages and access certain resources. To ensure that only the trusted parties can read the messages and resources, some form of encryption is typically used. One emergent technology is attribute-based encryption which is described in section [ABE].
To ensure that only trusted parties can access the data, some form of access control is often implemented. One emergent technology in this field is attribute-based access control described in section [ABAC]. The relatively new model of access control called NGAC is also introduced and is described in section [NGAC].

## Attribute-based Access Control - ABAC

Attribute-based Access Control (ABAC) is an access control model that performs a set of operations based on assigned attributes. These attributes are associated with one of the following categories: user attributes, object attributes, environmental attributes, connection attributes and administrative attributes. The attributes are used to determine if the user should be granted access or not. This allows for more flexible and fine-grained control over access control resources. For example, if a user wants to access a sensitive file, ABAC may check the user's role, the time of the day and the location to determine if the user should have access or not.

The disadvantages of ABAC are that it doesn't present a visual representation of the relationships between users and their attributes. It is also rather complicated to configure which can be problematic when storing a lot of information since it is hard to manage.

## Next Generation Access Control - NGAC

Next-generation access control or NGAC is a new access control model that is based on the idea of attributes. See section [ABAC] for more information about attributes.
NGAC was first proposed by NIST in 2018 [4] and is a more general, expressive and flexible model than ABAC.
NGACs policies are defined as a graph, where, each user attribute can have connections to an object attribute, this is read/write access or similar. Each user has a graph of the attributes that it has, so if you try to walk the path along the user's graph to the resource, you will either, reach the resource or not. If the resource is reached, then grant access else, do not. This is quite efficient and flexible since the only thing you need to do to revoke access for a user attribute to an object attribute removes the link between them. Moreover, it also yields maintainability benefits if using some sort of [graphical interface](https://github.com/esen96/ngac-graph-ui).

## Attribute-based Encryption - ABE

ABE stands for Attribute-Based Encryption. It is a type of encryption method in computer science that allows a user to encrypt data using attributes, such as a user's identity or a specific access level. This type of encryption is useful in settings where multiple users have different levels of access to sensitive data, as it allows the data to be encrypted in such a way that only users with the appropriate attributes can decrypt and access it. It is a public key encryption mechanism designed with group decryption goals rather than single users.
%This mechanism evolved from the older identity-based encryption (IBE) schemes.

## How do they work together?

So far, the systems do not work together, though, in theory, they could.
That is what this project is about.  For further reading on the subject, refer to the internal documentation in the [`docs`](./docs/) directory.

## Repository Structure

The repository is structured as follows:

```bash
|- docs/                    # Internal documentation
|  |- standards/            # Standards documents
|  |- design/               # Design documents
|  |- workflow/             # Workflow documents
|  |- sota/                 # State of the art documents
|  |- ISSUE_TEMPLATE        # Issue template
|  |- PULL_REQUEST_TEMPLATE # Pull request template
|- .github/                 # Github specific files
|  |- workflows/            # Github workflows
|- src/                     # Source code
|  |- API/                  # API helper library (installed as a package)
|  |- NgacApi/              # NGAC API source code (installed as a package)
|  |- interface_layer/      # Interface layer source code
|  |- app/                  # App source code
|- README.md                # This file
|- .gitignore               # Git ignore file
|- .gitmodules              # Git submodules
|- dependencies.txt         # Dependencies file
|- setup.bash               # Setup script ( for linux )
|- setup.ps1                # Setup script ( for windows )
|- setup.py                 # Setup tool ( ran by setup scripts )

```

## References

[1] Chiquito, Alex. Attribute-based Approaches for Secure Data Sharing in Industry. Luleå University of Technology, 2022

[2] [Rance DeLong. NGAC policy tool, policy server, and EPP.](https://github.com/tog-rtd/tog-ngac-crosscpp)

[3] Shai Fernandez, Eric Chiquito, Ulf Bodin. Federated system for contractual interactions and auctions.,Luleå University of Technology, 2020

[4] [Ferraiolo. NEXT GENERATION ACCESS CONTROL SYSTEM AND PROCESS FOR CONTROLLING DATABASE ACCESS.](https://patents.google.com/patent/US10127393B2/en)

[5] [Fraunhofer-AISEC. rabe.](https://github.com/Fraunhofer-AISEC/rabe)

[6] [PyO3. pyo3.](https://github.com/PyO3/pyo3)
