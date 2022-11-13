"""
    NGAC resource abstraction class

    This class is used to implement resources
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


class Resource(NgacObject):
    def __init__(self, resource: str):
        self.resource = resource

    def get_res(self) -> str:
        return self.resource


def test_create_resource():
    """
    Tests the creation of a resource
    """
    resource = Resource("test_resource")

    assert resource.get_res() == "test_resource"
