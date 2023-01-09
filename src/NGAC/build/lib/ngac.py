"""
    NGAC server wrapper class
    ---

    This file provides an interface to the NGAC server, allowing the user to
    set and get policies, and to switch between policies.
    
"""

from typing import List
import sys

import requests
import os

base_dir_changed = False
from endpoints import *
from info import *
from ngac_types import *
from ngac_types.ngac_object import NgacObject as NgacType
from ngac_types.ngac_policy import Policy
from ngac_types.user import User
from ngac_types.resource import Resource
from ngac_types.policy_element import PolicyElement
from access_request import AccessRequest


class NGAC:
    """
    NGAC server wrapper class
    ---

    Wraps the entire NGAC execution and provides an interface to the NGAC server.

    ## Examples

    ### Start and stop the NGAC server

    ```python
    ngac = NGAC()
    ngac.start()
    ngac.stop()
    ```
    ### Changing between policies

    ```python
    with NGAC() as ngac:
        ngac.switch_to(Policy("a"))
        ngac.get(Policy)
    ```
    """

    def __init__(self, policy_server_url="http://localhost:8001", token="") -> None:
        """
        Initialize the NGAC class

        :param policy_server_url: The url of the policy server
        :return: None

        ### Example:
        ```python
        with NGAC() as ngac:
            ngac.switch_to(Policy("test"))
        ```
        """
        if policy_server_url.endswith("/"):
            raise ValueError("The policy server url should not end with a /")
        self.policy_server_url = policy_server_url
        self.running = False
        self.token = token

    def url(self, endpoint: Endpoint) -> str:
        """
        Build a url from a given endpoint
        """
        return f"{self.policy_server_url}{endpoint}"

    ##########################################################
    #                        Checkers                        #
    ##########################################################
    def validate(self, access_request: AccessRequest) -> bool:
        """
        Validate an access request

        :param access_request: The access request to validate
        :return: True if the access request is valid, False otherwise
        """

        info(
            InfoTypes(),
            f"Validating {str(access_request[0])} => {access_request[1]} => {str(access_request[2])}",
        )
        params = {
            "user": access_request[0].id,
            "object": access_request[2].id,
            "ar": access_request[1],
            "token": self.token,
        }
        response = requests.get(self.url(Access()), params=params)
        print(response.text)
        return "grant" in response.text

    ##########################################################
    #                        Getters                         #
    ##########################################################
    def get(self, type: NgacType) -> requests.Response:
        """
        Generic get method for the NGAC server

        :param type: The type of request to make
        :return: The response from the NGAC server
        """
        if type == Policy:
            return self.get_policy()

    def get_policy(self) -> requests.Response:
        """
        Get the policy from the NGAC server
        :return: The response from the NGAC server

        ### Example:
        ```python
        with NGAC() as ngac:
            ngac.get(Policy)
        ```
        """
        # This is bad, we should make the user pass a token
        params = {"token": self.token}
        return requests.get(self.url(GetPolicy()), params=params)

    def read(self, policy: Policy = None) -> requests.Response:
        """
        Returns the details of a policy.
        ---

        If no policy is specified then it will return the currently loaded policy.
        If, however, a policy is specified then it will return that policies specification.
        """
        params = (
            {
                "token": f"{self.token}",
            }
            if policy == None
            else {"token": f"{self.token}", "policy": f"{policy.name}"}
        )

        return requests.get(self.url(ReadPolicy()), params=params)

    ##########################################################
    #                        Modifiers                       #
    ##########################################################

    def remove(
        self, element: PolicyElement, target_policy: Policy = None
    ) -> requests.Response:
        """
        Removes a single element from a policy
        """
        if type(element) is User or type(element) is Resource:
            return self.add_multiple(element, target_policy)

        params = (
            {
                "token": f"{self.token}",
                "policy_element": element.pol_el_repr(),
            }
            if target_policy == None
            else {
                "token": f"{self.token}",
                "policy_element": element.pol_el_repr(),
                "policy": f"{target_policy}",
            }
        )

        return requests.get(self.url(Delete()), params=params)

    def remove_multiple(self, element: PolicyElement, target_policy: Policy = None):
        """
        Removes a set of elements from a policy
        """
        params = (
            {
                "token": f"{self.token}",
                "policy_elements": element.pol_el_repr(),
            }
            if target_policy == None
            else {
                "token": f"{self.token}",
                "policy_elements": element.pol_el_repr(),
                "policy": f"{target_policy}",
            }
        )

        return requests.get(self.url(DeleteMultiple()), params=params)

    def add(
        self, element: PolicyElement, target_policy: Policy = None
    ) -> requests.Response:

        if type(element) is User or type(element) is Resource:
            return self.add_multiple(element, target_policy)

        params = (
            {
                "token": f"{self.token}",
                "policy_element": element.pol_el_repr(),
            }
            if target_policy == None
            else {
                "token": f"{self.token}",
                "policy_element": element.pol_el_repr(),
                "policy": f"{target_policy}",
            }
        )

        return requests.get(self.url(Add()), params=params)

    def add_multiple(self, element: PolicyElement, target_policy: Policy = None):
        params = (
            {
                "token": f"{self.token}",
                "policy_elements": element.pol_el_repr(),
            }
            if target_policy == None
            else {
                "token": f"{self.token}",
                "policy_elements": element.pol_el_repr(),
                "policy": f"{target_policy}",
            }
        )

        return requests.get(self.url(AddMultiple()), params=params)

    def change_policy(self, target_policy: NgacType) -> requests.Response:
        """
        Changes the policy of the NGAC server, these policies are stored in the policy server
        :param target_policy: The policy to switch to
        :return: The response from the NGAC server

        ### Example:
        ```python
        with NGAC() as ngac:
            ngac.switch_to(Policy("test"))
        ```
        """
        if target_policy.path is not None:
            # We need to load the policy first
            assert self.load_policy(path=target_policy.path).status_code == 200
        params = {"policy": str(target_policy), "token": f"{self.token}"}
        return requests.get(self.url(SetPolicy()), params=params)

    def load_policy(self, path="") -> requests.Response:
        """
        Loads a policy from file on the NGAC server
        :return: The response from the NGAC server
        """
        params = {"policyfile": f"{path}", "token": f"{self.token}"}
        return requests.get(self.url(LoadPolicy()), params=params)

    def load_policy_from_str(
        self, pol: str
    ) -> requests.Response:  # This should be replaced a function that loads from some python policy representation
        """
        Loads a policy from a string representation
        """
        params = {"policyspec": pol, "token": self.token}
        return requests.get(self.url(LoadImmediate()), params=params)

    def combine_policies(
        self, policies: List[Policy], target_policy: Policy
    ) -> requests.Response:
        """
        Combines a set of policies into one policy
        """
        if policies is None or len(policies) == 0:
            raise ValueError("The policies list is empty")
        for index in range(1, len(policies)):
            intermediate_policy = Policy(f"intermediate_policy")
            intermediate_policy = (
                str(intermediate_policy)
                if index < len(policies) - 1
                else str(target_policy)
            )
            params = {
                "policy1": str(policies[index - 1])
                if index == 1
                else str(intermediate_policy),
                "policy2": str(policies[index]),
                "combined": intermediate_policy,
                "token": f"{self.token}",
            }
            info(
                InfoTypes(),
                f"Combining: {str(policies[index-1])} and {str(policies[index])} => {str(intermediate_policy)}",
            )
            res = requests.get(self.url(CombinePolicy()), params=params)
        return res

    def change_context(self, context: List[str], token: str = "") -> requests.Response:
        """
        Changes the context in the epp to the given context
        """
        params = {
            "context": f"[{','.join(context)}]",
            "token": token if token != "" else self.token,
        }
        print(params)
        return requests.get(self.url(ContextNotify()), params=params)

    ##########################################################
    #                        Generics                        #
    ##########################################################
    def generic_request(self, endpoint, params: dict) -> requests.Response:
        base_url = f"{self.policy_server_url}{endpoint}"
        return requests.get(base_url, params=params)
