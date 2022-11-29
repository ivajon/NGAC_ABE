"""
    NGAC attribute abstraction class

    This class is used to implement attributes
"""


from .ngac_object import NgacObject


class Attribute(NgacObject):
    def __init__(self, attr: str):
        self.attr = attr

        super.__init__("Attribute")

    def get_attr(self) -> str:
        return self.attr
