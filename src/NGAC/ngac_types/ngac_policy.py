"""
    NGAC policy abstraction class

    This class is used to implement policies
"""

from .ngac_object import NgacObject


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
