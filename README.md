# Next Generation Access Control (NGAC) enabled by Attribute-Based Encryption (ABE)

[![Unit Tests](https://github.com/ivario123/NGAC_ABE/actions/workflows/unit_tests.yml/badge.svg?branch=ngac_boilerplate)](https://github.com/ivario123/NGAC_ABE/actions/workflows/unit_tests.yml) [![SpellCheck](https://github.com/ivario123/NGAC_ABE/actions/workflows/spellcheck.yml/badge.svg?branch=ngac_boilerplate)](https://github.com/ivario123/NGAC_ABE/actions/workflows/spellcheck.yml) [![Lint](https://github.com/ivario123/NGAC_ABE/actions/workflows/lint.yml/badge.svg?branch=ngac_boilerplate)](https://github.com/ivario123/NGAC_ABE/actions/workflows/lint.yml)

Here we should have some good filler text.

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
|- src/                     # Source code
|  |- tests/                # Unit tests
|  |- NGAC/                 # NGAC source code
|  |  |- ngac_types/        # NGAC types
|- README.md                # This file
```
