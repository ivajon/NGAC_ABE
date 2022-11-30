"""
User abstraction
---

This file described a user abstraction, this user abstraction is intended to be used
with the `NGAC` abstraction.
"""
from typing import List

from .ngac_object import NgacObject
from .ngac_attribute import UserAttribute


class User(NgacObject):
    """
    User abstraction
    ---

    Simple user abstraction. A user is a set of some attributes and a user specific id.
    """

    def __init__(self, attributes: List[UserAttribute], id: str = ""):
        """
        Creates a new user.
        ---
        """
        self.id = id
        self.attributes = attributes

    def get_attributes(self) -> List[UserAttribute]:
        """
        Returns the user's attributes.
        """
        return self.attributes

    def id(self) -> str:
        """
        Returns the user id.
        """
        return self.id

    def __iter__(self):
        """
        Iterates over the user's attributes.
        """
        return iter(self.attributes)

    def append(self, attribute: UserAttribute):
        """
        Appends an attribute to the user.
        """
        self.attributes.append(attribute)

    def remove(self, attribute: UserAttribute):
        """
        Removes an attribute from the user.
        """
        self.attributes.remove(attribute)

    def pop(self, index: int) -> UserAttribute:
        """
        Pops an attribute from the user.
        """
        return self.attributes.pop(index)

    def push(self, attribute: UserAttribute):
        """
        Pushes an attribute to the user.
        """
        self.attributes.append(attribute)

    def __len__(self) -> int:
        return len(self.attributes)

    def __getitem__(self, index: int) -> UserAttribute:
        return self.attributes[index]

    def __str__(self) -> str:
        return f"User: {self.id}, Attributes: {self.attributes}"


def test_create_user():
    """
    Test user creation.
    """
    user = User([], id="SomeUser")
    assert user.id == "SomeUser"


def test_create_with_attributes():
    """
    Test user creation with attributes.
    """
    attributes = [
        UserAttribute("value1"),
        UserAttribute("value2"),
        UserAttribute("value3"),
    ]
    user = User(attributes, id="SomeUser")
    assert user.id == "SomeUser"
    assert user.get_attributes() == attributes


def test_list_like_user():
    """
    Test user class, list like operations.
    """
    attributes = [
        UserAttribute("value1"),
        UserAttribute("value2"),
        UserAttribute("value3"),
    ]
    user = User(attributes, id="SomeUser")

    assert user[0] == attributes[0]
    assert user[1] == attributes[1]

    assert len(user) == 3
    popped = user.pop(0)
    assert popped == UserAttribute("value1")
    assert len(user) == 2
    user.push(UserAttribute("value4"))
    assert len(user) == 3
    assert user[2] == UserAttribute("value4")

    for attribute in user:
        assert attribute in attributes or attribute == UserAttribute("value4")

    user.remove(UserAttribute("value4"))
    assert len(user) == 2
    user.append(UserAttribute("value4"))
    assert len(user) == 3


if __name__ == "__main__":
    test_create_user()
    test_create_with_attributes()
    test_list_like_user()
