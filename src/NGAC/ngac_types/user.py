"""
User abstraction

This class is used to implement users
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


UA = relative_import("ngac_attribute", "UserAttribute")
NgacObject = relative_import("ngac_object", "NgacObject")


from typing import List


class User(NgacObject):
    """
    User abstraction

    it's possible to itterate over a user's attributes

    Example:
    ```python
    for attr in user:
        print(attr)
    ```
    """

    def __init__(self, attributes: List[UA], id: str = ""):
        self.id = id
        self.attributes = attributes
        #super.__init__("User")

    def __iter__(self):
        return iter(self.attributes)

    def append(self, attr: UA):
        """
        Appends an attribute to the user
        """
        self.attributes.append(attr)

    def remove(self, attr: UA):
        """
        Removes an attribute from the user
        """
        self.attributes.remove(attr)

    def pop(self, index: int) -> UA:
        """
        Pops an attribute from the user
        """
        return self.attributes.pop(index)

    def push(self, attr: UA):
        """
        Pushes an attribute to the user
        """
        self.attributes.append(attr)

    def get_attributes(self) -> List[UA]:
        return self.attributes

    def id(self) -> str:
        """
        Returns the user id
        """
        return self.id
