"""
    NGAC attribute abstraction class

    This class is used to implement attributes
"""


def relative_import(package, module):
    """
    Solves pythons relative import problem
    """
    import os

    exec(
        f"""from {"" if os.getcwd().endswith("ngac_types") else "ngac_types." if os.getcwd().endswith("NGAC") else "NGAC.ngac_types."}{package} import {module}"""
    )
    return locals()[module]


NgacObject = relative_import("ngac_object", "NgacObject")


class Attribute(NgacObject):
    """
    NGAC attribute abstraction class

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


class ObjectAttribute(Attribute):
    """
    ObjectAttribute abstraction

    Serves typing purposes
    """

    def __init__(self, object_attribute: str):
        # super.__init__(obj_attr)
        self.object_attribute = object_attribute

    def __str__(self) -> str:
        return self.object_attribute


class UserAttribute(Attribute):
    """
    UserAttribute abstraction

    Serves typing purposes
    """

    def __init__(self, user_attr: str):
        self.user_attr = user_attr

    def __str__(self) -> str:
        return self.user_attr


def test_ngac_attribute():
    """
    Test attribute class
    """
    attr = ObjectAttribute("SomeAttribute")
    assert attr.get_attribute() == "SomeAttribute"

    attr2 = UserAttribute("SomeAttribute")
    assert attr2.get_attribute() == "SomeAttribute"

    assert attr == attr2
