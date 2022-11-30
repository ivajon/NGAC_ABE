"""
    NGAC server wrapper class
    ---

    This class allows the NGAC server to be started and stopped
    in a with statement. This ensures that the server is always stopped
    and never left running.

    It also provides an interface to the NGAC server, allowing the user to
    set and get policies, and to switch between policies.

    ## Example
    ```python
    with NGAC() as ngac:
        ngac.switch_to(Policy ("a"))
        ngac.get(Policy)
    ```
    
"""

from typing import List
import sys

import requests
import os

base_dir_changed = False
if os.getcwd().endswith("src"):
    os.chdir("NGAC")
    base_dir_changed = True
from api import *
from info import *
from ngac_types import *
from ngac_types.ngac_object import NgacObject as NgacType
from ngac_types.ngac_policy import Policy
from ngac_types.user import User
from ngac_types.resource import Resource
from access_request import AccessRequest

if base_dir_changed:
    os.chdir("..")


def exception_hook(exctype, value, traceback) -> None:
    """
    This function is called when an exception is raised

    It ensures that the NGAC server is stopped and that all trailing subprocesses
    are killed. It does risk killing other processes, but this is a risk that is not that problematic
    in the development environment.

    This should be replaced with a more robust solution in production.
    """
    print(f"Exception: {exctype}")
    print(f"Value: {value}.")
    print(f"Traceback: {traceback}.")
    import subprocess

    info(Error(), "An exception was raised. Stopping the NGAC server")
    info(
        Error(),
        f"Exception: {exctype}\nValue: {value}\nTraceback: {traceback}",
        File("crash.log"),
    )
    import os

    if os.name == "nt":
        # Kill all processes running under swipl
        subprocess.run(["taskkill", "/F", "/IM", "swipl.exe"])

        # Kill all processes running under python
        subprocess.run(["taskkill", "/F", "/IM", "python.exe"])
    else:
        # Kill all processes running under swipl
        subprocess.run(["killall", "swipl"])

        # Kill all processes running under python
        subprocess.run(["killall", "python"])


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

    def __init__(
        self,
        policy_server_url="http://localhost:8001",
    ) -> None:
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
        sys.excepthook = exception_hook

    ##########################################################
    #                        Checkers                        #
    ##########################################################
    def validate(self, access_request: AccessRequest, token: str = "") -> bool:
        """
        Validate an access request

        :param access_request: The access request to validate
        :return: True if the access request is valid, False otherwise
        """

        info(
            InfoTypes(),
            f"Validating {str(access_request[0])} =>{access_request[1]}=> {str(access_request[2])}",
        )
        base_url = f"{self.policy_server_url}{Access()}"
        params = {
            "user": access_request[0].id,
            "object": access_request[2].id,
            "ar": access_request[1],
            "token": token,
        }
        response = requests.get(base_url, params=params)
        print(response.text)
        return "grant" in response.text

    ##########################################################
    #                        Getters                         #
    ##########################################################
    def get(self, type: NgacType, token: str) -> requests.Response:
        """
        Generic get method for the NGAC server

        :param type: The type of request to make
        :return: The response from the NGAC server
        """
        if type == Policy:
            return self.get_policy(token=token)

    def get_policy(self, token: str = "") -> requests.Response:
        """
        Get the policy from the NGAC server
        :return: The response from the NGAC server

        ### Example:
        ```python
        with NGAC() as ngac:
            ngac.get(Policy)
        ```
        """
        base_url = f"{self.policy_server_url}{GetPolicy()}"
        # This is bad, we should make the user pass a token
        params = {"token": f"{token}"}
        return requests.get(base_url, params=params)

    ##########################################################
    #                        Setters                         #
    ##########################################################
    def switch_to(self, value: NgacType, token: str = "") -> requests.Response:
        """
        Generic switch to method for the NGAC server

        :param value: The value to switch to
        :return: The response from the NGAC server

        ### Example:
        ```python
        with NGAC() as ngac:
            ngac.switch_to(Policy("test"))
        ```
        """
        if type(value) == Policy:
            return self.switch_to_policy(value, token=token)

    def switch_to_policy(self, policy: Policy, token: str = "") -> requests.Response:
        """
        Changes the policy of the NGAC server, these policies are stored in the policy server
        :param policy: The policy to switch to
        :return: The response from the NGAC server

        ### Example:
        ```python
        with NGAC() as ngac:
            ngac.switch_to(Policy("test"))
        ```
        """
        if policy.path is not None:
            # We need to load the policy first
            assert self.load_policy(policy.path, token=token).status_code == 200
        base_url = f"{self.policy_server_url}{SetPolicy()}"
        params = {"policy": str(policy), "token": f"{token}"}
        info(InfoTypes(), f"Switching to policy NGAC server: {str(policy)}")
        return requests.get(base_url, params=params)

    def load(self, item: NgacType, token: str = "") -> requests.Response:
        """
        Generic load method for the NGAC server

        :param item: The item to load
        :return: The response from the NGAC server
        """
        if type(item) == Policy:
            # We now know that item is a policy
            if item.path is None:
                raise ValueError("The path of the policy is not set")
            return self.load_policy(path=item.path, token=token)

    def load_policy(self, path="", token: str = "") -> requests.Response:
        """
        Loads a policy from file on the NGAC server
        :return: The response from the NGAC server
        """

        base_url = f"{self.policy_server_url}{LoadPolicy()}"
        params = {"policyfile": f"{path}", "token": f"{token}"}
        info(InfoTypes(), f"Loading: {path.split('/')[-1]}")
        res = requests.get(base_url, params=params)
        print(res.text)
        return res

    ##########################################################
    #                        Modifiers                       #
    ##########################################################
    def combine_policies(
        self, policies: List[Policy], target_policy: Policy, token: str = ""
    ) -> requests.Response:
        """
        Combines a set of policies into one policy
        """
        if policies is None or len(policies) == 0:
            raise ValueError("The policies list is empty")
        base_url = f"{self.policy_server_url}{CombinePolicy()}"
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
                "token": f"{token}",
            }
            info(
                InfoTypes(),
                f"Combining: {str(policies[index-1])} and {str(policies[index])} => {str(intermediate_policy)}",
            )
            res = requests.get(base_url, params=params)
        return res

    ##########################################################
    #                        Context                         #
    ##########################################################

    def start(self) -> None:
        """
        Start the NGAC server
        """
        # Start all the executables as subprocesses
        import os
        import subprocess

        self.runners = subprocess.Popen(
            ["python", "__main__.py"],
            cwd="./NGAC/executables"
            if os.getcwd().endswith("src")
            else "./executables",
        )
        self.running = True

    def stop(self) -> None:
        """
        Stop the NGAC server
        """
        self.runners.terminate()
        # Wait for the subprocesses to stop
        self.runners.wait()
        self.running = False
        import os
        import subprocess

        if os.name == "nt":
            # Kill all processes running under swipl
            subprocess.run(["taskkill", "/F", "/IM", "swipl.exe"])
        else:
            # Kill all processes running under swipl
            subprocess.run(["killall", "swipl"])

    def __enter__(self) -> "NGAC":
        info(InfoTypes(), "Starting NGAC server")
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, exc_tb) -> None:
        info(InfoTypes(), "Stopping NGAC server")
        self.stop()
