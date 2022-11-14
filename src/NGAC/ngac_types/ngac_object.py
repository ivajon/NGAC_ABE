"""
    NGAC Object class

    This is a super class which the other types will inherit from. 
"""


class NgacObject:
    def __init__(self, type: str):
        self.type = type

    def get_type(self) -> str:
        return self.type


def test_ngac_object():
    """
    Test NGAC object class
    """
    ngac_object = NgacObject("NgacObject")
    assert ngac_object.get_type() == "NgacObject"
