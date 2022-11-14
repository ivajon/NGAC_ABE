"""
    NGAC policy abstraction class

    This class is used to implement policies
"""

from .ngac_object import NgacObject


class Policy(NgacObject):
    def __init__(self, path: str = None, name: str = None):
        """
        Creates a new policy
        :param path: the path to the policy
        :param name: the name of the policy
        """
        self.name = name
        self.path = path

    def get_path(self) -> str:
        """
        Returns the path to the policy
        """
        return self.path

    def __str__(self) -> str:
        return self.name


def test_create_policy():
    """
    Tests the creation of a policy
    """
    policy = Policy(name="test_policy")

    assert policy.get_path() == None
