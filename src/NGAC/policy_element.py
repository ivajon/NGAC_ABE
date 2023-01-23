"""
Policy element
---

Generic representation of a "Policy Element".

## Policy element

A policy element can be:
- User declaration
- Resource declaration 
- Attribute assignment
- Attribute relation
"""


class PolicyElement:
    """
    Policy element
    ---

    A policy element wrapper, this can be attribute assignments and similar
    """

    def pol_el_repr(self) -> str:
        return ""
