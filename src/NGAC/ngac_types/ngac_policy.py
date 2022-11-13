"""
    NGAC policy abstraction class

    This class is used to implement policies
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


class Policy(NgacObject):
    def __init__(self, policy: str):
        self.policy = policy

    def get_pol(self) -> str:
        return self.policy


def test_create_policy():
    """
    Tests the creation of a policy
    """
    policy = Policy("test_policy")

    assert policy.get_pol() == "test_policy"
