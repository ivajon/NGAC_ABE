"""
Policy
---

This file describes a simple policy abstraction. It assumes that the policy already exists on the server.
"""

from .ngac_object import NgacObject


class Policy(NgacObject):
    def __init__(self, path: str = None, name: str = None):
        """
        Creates a new policy.
        """
        self.name = name
        self.path = path

    def get_path(self) -> str:
        """
        Returns the path to the policy.
        """
        return self.path

    def __str__(self) -> str:
        return self.name


def test_create_policy():
    """
    Tests the creation of a policy.
    """
    policy = Policy(name="test_policy")

    assert policy.get_path() == None
