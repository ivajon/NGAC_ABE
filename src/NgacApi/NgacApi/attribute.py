"""
NGAC attribute
---

This file describes a simple attribute abstraction as well as 2 wrapper classes that are used for the `User` and `Resource` classes.

The `Attribute` class it self should never be used.
"""


from .ngac_object import NgacObject
from .policy_element import PolicyElement


class Attribute(NgacObject):
    """
    NGAC attribute abstraction class
    ---

    This class is only for typing.
    """

    def __str__(self) -> str:
        return ""

    def __repr__(self) -> str:
        return self.__str__()

    def get_attribute(self) -> str:
        return self.__str__()

    def __eq__(self, __o: "Attribute") -> bool:
        return self.__str__() == __o.__str__()  # They are just string wrappers

    def __hash__(self) -> int:
        return hash(self.__str__())


class ObjectAttribute(Attribute, PolicyElement):
    """
    ObjectAttribute abstraction
    ---

    Used to described attributes for `Resource`s.
    """

    def __init__(self, object_attribute: str):
        # super.__init__(obj_attr)
        self.object_attribute = object_attribute

    def __str__(self) -> str:
        return self.object_attribute

    def pol_el_repr(self) -> str:
        return f"object_attribute({self.object_attribute})"


class UserAttribute(Attribute, PolicyElement):
    """
    UserAttribute abstraction
    ---

    Used to describe attributes for `User`s.
    """

    def __init__(self, user_attr: str):
        self.user_attr = user_attr

    def __str__(self) -> str:
        return self.user_attr

    def pol_el_repr(self) -> str:
        return f"user_attribute({self.user_attr})"


def test_ngac_attribute():
    """
    Test attribute class.
    """
    attr = ObjectAttribute("SomeAttribute")
    assert attr.get_attribute() == "SomeAttribute"

    attr2 = UserAttribute("SomeAttribute")
    assert attr2.get_attribute() == "SomeAttribute"

    assert attr == attr2


def test_attr_repr():
    """
    Test attribute class.
    """
    attr = ObjectAttribute("SomeAttribute")
    assert attr.__repr__() == "SomeAttribute"

    attr2 = UserAttribute("SomeAttribute")
    assert attr2.__repr__() == "SomeAttribute"

    assert attr == attr2
    assert attr.__hash__() == attr2.__hash__()
    assert attr.__str__() == attr2.__str__()
