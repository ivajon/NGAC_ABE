# Next Generation Access Control (NGAC) enabled by Attribute-Based Encryption (ABE)

[![Unit Tests](https://github.com/ivario123/NGAC_ABE/actions/workflows/unit_tests.yml/badge.svg?branch=ngac_boilerplate)](https://github.com/ivario123/NGAC_ABE/actions/workflows/unit_tests.yml) [![SpellCheck](https://github.com/ivario123/NGAC_ABE/actions/workflows/spellcheck.yml/badge.svg?branch=ngac_boilerplate)](https://github.com/ivario123/NGAC_ABE/actions/workflows/spellcheck.yml) 

Here we should have some good filler text.

## Setup

Read the docs [readme](/docs/README.md)


## Prelude

### NGAC

NGAC is a system that allows you to perform access control based on a set of user attributes.

### ABE

Attribute-Based Encryption (ABE) is a system that allows you to encrypt data based on a set of user attributes.

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
