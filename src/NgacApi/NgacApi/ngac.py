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
import json


from .endpoints import *
from .info import *
from .ngac_object import NgacObject as NgacType
from .policy import Policy
from .user import User
from .resource import Resource
from .policy_element import PolicyElement
from .access_request import AccessRequest
from .errors import *


def http_ok(code: int) -> bool:
    """
    Checks if http status code is one of the OK ones
    """
    return code >= 200 and code < 300


def http_error(code: int) -> str:
    import http.client

    return http.client.responses[code]


class NGAC:
    """
    NGAC server wrapper class
    ---

    Wraps the entire NGAC execution and provides an interface to the NGAC server.

    # Examples

    # Start and stop the NGAC server

    ```python
    ngac = NGAC()
    ngac.start()
    ngac.stop()
    ```
    # Changing between policies

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

        # Example:
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
    def validate(self, access_request: AccessRequest) -> Result:
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
        if not http_ok(response.status_code):
            return Error(http_error(response.status_code))
        if response is None:
            return Error(NoServerResponse)

        resp = json.loads(response.text)
        if resp["respStatus"] == "Error":
            return Error(generic_NGAC_error(resp["respMessage"]))
        return Ok(resp["respMessage"] != "deny")

    ##########################################################
    #                        Getters                         #
    ##########################################################

    def get_policy(self) -> Result:
        """
        Get the policy from the NGAC server
        :return: The response from the NGAC server

        # Example:
        ```python
        ```
        """
        # This is bad, we should make the user pass a token
        params = {"token": self.token}

        response = requests.get(self.url(GetPolicy()), params=params)
        if not http_ok(response.status_code):
            return Error(http_error(response.status_code))
        if response is None:
            return Error(NoServerResponse)

        resp = json.loads(response.text)
        if resp["respStatus"] == "Error":
            return Error(generic_NGAC_error(resp["respMessage"]))
        # prin(Ok(resp["respMessage"]))
        return Ok(resp["respBody"])

    def read(self, policy: Policy) -> Result:
        """
        Returns the details of a policy.
        ---

        If no policy is specified then it will return the currently loaded policy.
        If, however, a policy is specified then it will return that policies specification.
        """
        params = ({"token": f"{self.token}", "policy": f"{policy.name}"})
        response = requests.get(self.url(ReadPolicy()), params=params)
        if not http_ok(response.status_code):
            return Error(http_error(response.status_code))
        if response is None:
            return Error(NoServerResponse)

        resp = json.loads(response.text)
        if resp["respStatus"] == "Error":
            return Error(generic_NGAC_error(resp["respMessage"]))
        return Ok(resp["respBody"])

    ##########################################################
    #                        Modifiers                       #
    ##########################################################

    def remove_generic(self, element: str, target_policy: Policy = None) -> Result:
        """
        Removes a single element from a policy
        ---

        This function is used to remove a single element from a policy,
        provided that the element is a valid NGAC element.
        """
        params = (
            {
                "token": f"{self.token}",
                "policy_element": element,
            }
            if target_policy == None
            else {
                "token": f"{self.token}",
                "policy_element": element,
                "policy": f"{target_policy}",
            }
        )

        response = requests.get(self.url(Delete()), params=params)
        if not http_ok(response.status_code):
            return Error(http_error(response.status_code))
        if response is None:
            return Error(NoServerResponse)

        resp = json.loads(response.text)
        if resp["respStatus"] == "Error":
            return Error(generic_NGAC_error(resp["respMessage"]))
        # prin(Ok(resp["respMessage"]))
        return Ok(resp["respMessage"])

    def remove(self, element: PolicyElement, target_policy: Policy = None) -> Result:
        """
        Removes a single element from a policy
        """
        if type(element) is User or type(element) is Resource:
            return self.remove_multiple(element, target_policy)

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

        response = requests.get(self.url(Delete()), params=params)
        if not http_ok(response.status_code):
            return Error(http_error(response.status_code))
        if response is None:
            return Error(NoServerResponse)

        resp = json.loads(response.text)
        if resp["respStatus"] == "Error" or resp["respStatus"] == "failure":
            return Error(generic_NGAC_error(resp["respMessage"]))
        # prin(Ok(resp["respMessage"]))
        return Ok(resp["respMessage"])

    def remove_multiple(
        self, element: PolicyElement, target_policy: Policy = None
    ) -> Result:
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

        response = requests.get(self.url(DeleteMultiple()), params=params)
        if not http_ok(response.status_code):
            return Error(http_error(response.status_code))
        if response is None:
            return Error(NoServerResponse)
        resp = json.loads(response.text)
        if resp["respStatus"] == "Error":
            return Error(generic_NGAC_error(resp["respMessage"]))
        return Ok(resp["respMessage"])

    def add_generic(self, element: str, target_policy: Policy = None) -> Result:
        """
        Adds a single element to a policy
        ---
        This function is used to add a single element to a policy,
        provided that the element is a valid NGAC element.
        """
        params = (
            {
                "token": f"{self.token}",
                "policy_element": element,
            }
            if target_policy == None
            else {
                "token": f"{self.token}",
                "policy_element": element,
                "policy": f"{target_policy}",
            }
        )

        response = requests.get(self.url(Add()), params=params)
        if not http_ok(response.status_code):
            return Error(http_error(response.status_code))
        if response is None:
            return Error(NoServerResponse)

        resp = json.loads(response.text)
        if resp["respStatus"] == "Error":
            return Error(generic_NGAC_error(resp["respMessage"]))
        return Ok(resp["respBody"])

    def remove_assignment(self, a: PolicyElement, b: PolicyElement, target_policy: Policy) -> Result:
        """
        Removes an assignment from a policy
        ---

        This function is used to remove an assignment from a policy,
        provided that the assignment is a valid NGAC assignment.
        """

        params = (
            {
                "token": f"{self.token}",
                "policy_element": f"assign({a.id},{b})",
                "policy": f"{target_policy}",
            }
        )
        response = requests.get(self.url(Delete()), params=params)
        if not http_ok(response.status_code):
            return Error(http_error(response.status_code))
        if response is None:
            return Error(NoServerResponse)
        resp = json.loads(response.text)
        if resp["respStatus"] == "failure" or resp["respStatus"] == "Error":
            return Error(generic_NGAC_error(resp["respMessage"]))
        return Ok(resp["respMessage"])

    def add(self, element: PolicyElement, target_policy: Policy = None) -> Result:
        """
        Adds a single element to a policy
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

        response = requests.get(self.url(Add()), params=params)
        if not http_ok(response.status_code):
            return Error(http_error(response.status_code))
        if response is None:
            return Error(NoServerResponse)
        resp = json.loads(response.text)
        if resp["respStatus"] == "Error" or resp["respStatus"] == "failure":
            return Error(generic_NGAC_error(resp["respMessage"]))
        # prin(Ok(resp["respMessage"]))
        return Ok(resp["respMessage"])

    def add_multiple(
        self, element: PolicyElement, target_policy: Policy = None
    ) -> Result:
        """
        Adds a set of elements to a policy
        ---

        Allows the user to add multiple elements to a policy in one go, This is useful for adding users and resources.
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

        response = requests.get(self.url(AddMultiple()), params=params)
        if not http_ok(response.status_code):
            return Error(http_error(response.status_code))
        if response is None:
            return Error(NoServerResponse)
        resp = json.loads(response.text)
        if resp["respStatus"] == "Error" or resp["respStatus"] == "failure":
            return Error(generic_NGAC_error(resp["respMessage"]))
        # prin(Ok(resp["respMessage"]))
        return Ok(resp["respMessage"])

    def assign(self, a: PolicyElement, b: PolicyElement, target_policy: Policy = None) -> Result:
        """
        Assigns an element to another element
        ---

        This function is used to assign an element to another element,
        provided that the assignment is a valid NGAC assignment.
        """

        params = (
            {
                "token": f"{self.token}",
                "policy_element": f"assign({a.id},{b.pol_el_repr()})",
            }
            if target_policy == None
            else {
                "token": f"{self.token}",
                "policy_element": f"assign({a.id},{b})",
                "policy": f"{target_policy}",
            }
        )
        response = requests.get(self.url(Add()), params=params)
        if not http_ok(response.status_code):
            return Error(http_error(response.status_code))
        if response is None:
            return Error(NoServerResponse)
        resp = json.loads(response.text)
        if resp["respStatus"] == "Error" or resp["respStatus"] == "failure":
            return Error(generic_NGAC_error(resp["respMessage"]))
        return Ok(resp["respMessage"])

    def change_policy(self, target_policy: NgacType) -> Result:
        """
        Changes the policy of the NGAC server
        ---

        Allows changing to a loaded policy
        """
        if target_policy.path is not None:
            # We need to load the policy first
            unwrap(self.load_policy(path=target_policy.path))
        params = {"policy": str(target_policy), "token": f"{self.token}"}

        response = requests.get(self.url(SetPolicy()), params=params)
        if not http_ok(response.status_code):
            return Error(http_error(response.status_code))
        if response is None:
            return Error(NoServerResponse)
        resp = json.loads(response.text)
        if resp["respStatus"] == "Error" or resp["respStatus"] == "failure":
            return Error(generic_NGAC_error(resp["respMessage"]))
        return Ok(resp["respMessage"])

    def load_policy(self, path="") -> Result:
        """
        Loads a policy from file on the NGAC server
        ---
        """
        params = {"policyfile": f"{path}", "token": f"{self.token}"}
        response = requests.get(self.url(LoadPolicy()), params=params)
        if not http_ok(response.status_code):
            return Error(http_error(response.status_code))
        if response is None:
            return Error(NoServerResponse)
        resp = json.loads(response.text)
        if resp["respStatus"] == "Error" or resp["respStatus"] == "failure":
            return Error(generic_NGAC_error(resp["respMessage"]))
        return Ok(resp["respMessage"])

    def load_policy_from_policy(self, pol: Policy) -> Result:
        """
        Loads a policy from a policy object
        """
        params = {"policyspec": pol.full_representation(), "token": self.token}
        response = requests.get(self.url(LoadImmediate()), params=params)
        if response.status_code.is_error():
            return Error(http_error(response.status_code))
        if response is None:
            return Error(NoServerResponse)
        resp = json.loads(response.text)
        if resp["respStatus"] == "Error" or resp["respStatus"] == "failure":
            return Error(generic_NGAC_error(resp["respMessage"]))
        return Ok(resp["respMessage"])

    def load_policy_from_str(
        self, pol: str
    ) -> Result:  # This should be replaced a function that loads from some python policy representation
        """
        Loads a policy from a string representation
        """
        params = {"policyspec": pol, "token": self.token}
        response = requests.get(self.url(LoadImmediate()), params=params)
        if response.status_code < 200 or response.status_code > 299:
            return Error(http_error(response.status_code))
        if response is None:
            return Error(NoServerResponse)
        resp = json.loads(response.text)
        status = resp["respStatus"].lower()
        if status == "error" or status == "failure":
            return Error(generic_NGAC_error(resp["respMessage"]))
        return Ok(resp["respMessage"])

    def combine_policies(self, policies: List[Policy], target_policy: Policy) -> Result:
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
            if res is None:
                return Error(NoServerResponse)
            if not http_ok(res.status_code):
                return Error(http_error(res.status_code))
            resp = json.loads(res.text)
            if resp["respStatus"] == "Error":
                return Error(generic_NGAC_error(resp["respMessage"]))
        return Ok("Policies combined successfully")

    def change_context(self, context: List[str], token: str = "") -> Result:
        """
        Changes the context in the epp to the given context
        """
        params = {
            "context": f"[{','.join(context)}]",
            "token": token if token != "" else self.token,
        }
        response = requests.get(self.url(ContextNotify()), params=params)
        if not http_ok(response.status_code):
            return Error(http_error(response.status_code))
        if response is None:
            return Error(NoServerResponse)
        resp = json.loads(response.text)
        if resp["respStatus"] == "Error":
            return Error(generic_NGAC_error(resp["respMessage"]))
        return Ok(resp["respMessage"])

    ##########################################################
    #                        Generics                        #
    ##########################################################
    def generic_request(self, endpoint, params: dict) -> requests.Response:
        base_url = f"{self.policy_server_url}{endpoint}"
        return requests.get(base_url, params=params)
