"""
User abstraction

This class is used to implement users
"""
from typing import List


def relative_import(package, module):
    """
    Solves pythons relative import problem
    """
    import os

    exec(
        f"""from {"" if os.getcwd().endswith("ngac_types") else "ngac_types." if os.getcwd().endswith("NGAC") else "NGAC.ngac_types."}{package} import {module}"""
    )
    return locals()[module]


UserAttribute = relative_import("ngac_attribute", "UserAttribute")
NgacObject = relative_import("ngac_object", "NgacObject")


class User(NgacObject):
    """
    User abstraction

    A user supports most of the list methods

    Example:
    ```python
    for attribute in user:
        print(attribute)
    ```
    """

    def __init__(self, attributes: List[UserAttribute], id: str = ""):
        """
        Creates a new user
        :param attributes: the user's attributes
        :param id: the user's id, name or similar
        """
        self.id = id
        self.attributes = attributes

    def get_attributes(self) -> List[UserAttribute]:
        """
        Returns the user's attributes
        """
        return self.attributes

    def id(self) -> str:
        """
        Returns the user id
        """
        return self.id

    def __iter__(self):
        """
        Iterates over the user's attributes
        """
        return iter(self.attributes)

    def append(self, attribute: UserAttribute):
        """
        Appends an attribute to the user
        """
        self.attributes.append(attribute)

    def remove(self, attribute: UserAttribute):
        """
        Removes an attribute from the user
        """
        self.attributes.remove(attribute)

    def pop(self, index: int) -> UserAttribute:
        """
        Pops an attribute from the user
        """
        return self.attributes.pop(index)

    def push(self, attribute: UserAttribute):
        """
        Pushes an attribute to the user
        """
        self.attributes.append(attribute)

    def __len__(self) -> int:
        return len(self.attributes)

    def __getitem__(self, index: int) -> UserAttribute:
        return self.attributes[index]
