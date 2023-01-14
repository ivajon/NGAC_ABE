"""
Policy
---

This file describes a simple policy abstraction. It assumes that the policy already exists on the server.
"""

from typing import List
from .ngac_object import NgacObject
from .policy_element import PolicyElement


class Policy(NgacObject):
    """
    A policy is a set of rules that define the access control policy.
    """

    rules: List[PolicyElement | str] = []

    def __init__(
        self, path: str = None, name: str = None, rules: List[PolicyElement | str] = []
    ):
        """
        Creates a new policy.
        """
        self.name = name
        self.path = path
        self.rules = rules

    def get_path(self) -> str:
        """
        Returns the path to the policy.
        """
        return self.path

    def __str__(self) -> str:
        """
        Returns the name of the policy.
        """
        return self.name

    def append(self, polEl: PolicyElement):
        """
        Adds a new rule to the policy.
        """
        self.rules.append(polEl)

    def pop(self):
        """
        Removes the last rule from the policy.
        """
        return self.rules.pop()

    def get_rules(self) -> List[PolicyElement]:
        """
        Returns the rules of the policy.
        """
        return self.rules

    def remove(self, polEl: PolicyElement):
        """
        Removes a rule from the policy.
        """
        self.rules.remove(polEl)

    def full_representation(self) -> str:
        """
        Returns the full string representation of the policy.
        """
        ret = f"policy({self.name}),access,["
        for rule in self.rules:
            if isinstance(rule, str):
                ret += rule + ","
            else:
                ret += rule.pol_el_repr() + ","
        return ret[:-1] + "])"


def test_create_policy():
    """
    Tests the creation of a policy.
    """
    policy = Policy(name="test_policy")

    assert policy.get_path() == None
