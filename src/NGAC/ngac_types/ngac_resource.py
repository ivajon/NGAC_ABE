"""
    NGAC resource abstraction class

    This class is used to implement resources
"""

from ngac_object import NgacObject


class Resource(NgacObject):
    def __init__(self, res: str):
        self.res = res

        super.__init__("Resource")

    def get_res(self) -> str:
        return self.res
