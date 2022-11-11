"""
    NGAC attribute abstraction class

    This class is used to implement attributes
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
print(NgacObject)


class Attribute(NgacObject):
    def __init__(self, attr: str):
        self.attr = attr

        # super.__init__("Attribute")

    def get_attr(self) -> str:
        return self.attr


class ObjectAttribute(Attribute):
    """
    ObjectAttribute abstraction

    Serves typing purposes
    """

    def __init__(self, obj_attr: str):
        # super.__init__(obj_attr)
        self.obj_attr = obj_attr


class UserAttribute(Attribute):
    """
    UserAttribute abstraction

    Serves typing purposes
    """

    def __init__(self, user_attr: str):
        self.user_attr = user_attr
