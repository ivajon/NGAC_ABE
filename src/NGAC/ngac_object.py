"""
NGAC Object
---

This file implements a type level NgacObject. It it self should never be instantiated as it merely exists for
typing.
"""


class NgacObject:
    """
    Type level NGAC object.
    """

    def __init__(self, type: str):
        """
        This should never be instantiated.
        """
        self.type = type

    def get_type(self) -> str:
        """
        Returns the type of the object.
        """
        return self.type


def test_ngac_object():
    """
    Test NGAC object class.
    """
    ngac_object = NgacObject("NgacObject")
    assert ngac_object.get_type() == "NgacObject"
