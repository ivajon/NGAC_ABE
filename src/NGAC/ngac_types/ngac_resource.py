"""
Resource abstraction
---

This file contains a simple resource abstraction, this is agnostic to what the resource is, as long as it has a name.
"""

from ngac_object import NgacObject


class Resource(NgacObject):
    def __init__(self, res: str):
        self.res = res

        super.__init__("Resource")

    def get_res(self) -> str:
        return self.res
