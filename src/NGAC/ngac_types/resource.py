"""
Resource abstraction

A resource can be a file or something else
"""


def relative_import(package, module):
    """
    Solves pythons shitty relative import problem
    """
    import os

    exec(
        f"""from {"" if os.getcwd().endswith("ngac_types") else "ngac_types." if os.getcwd().endswith("NGAC") else "NGAC.ngac_types."}{package} import {module}"""
    )
    return locals()[module]


NgacObject = relative_import("ngac_object", "NgacObject")
OA = relative_import("ngac_attribute", "ObjectAttribute")

from typing import List


class Resource(NgacObject):
    """
    Resource abstraction

    it's possible to iterate over a resource's attributes

    Example:
    ```python
    for attr in resource:
        print(attr)
    ```

    A resource is much more static than a `user`
    """

    def __init__(self, attributes: List[OA], id: str = ""):
        self.id = id
        self.attributes = attributes
        # super.__init__("Resource")

    def __iter__(self):
        return iter(self.attributes)

    def get_resource(self) -> str:
        """
        Returns the resource id
        """
        return self.id
