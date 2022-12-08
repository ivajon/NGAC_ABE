import os

if os.getcwd().endswith("src"):
    from .ngac import NGAC
else:
    from ngac import NGAC


def test_combine_policies():
    """
    Test the combine policies method
    """
    if os.getcwd().endswith("src"):
        from NGAC.ngac import NGAC
        from NGAC.ngac_types.ngac_policy import Policy
        from NGAC.ngac_types.user import User
        from NGAC.ngac_types.resource import Resource
    else:
        from ngac import NGAC
        from ngac_types.ngac_policy import Policy
        from ngac_types.user import User
        from ngac_types.resource import Resource
    ngac = NGAC()
    import time

    time.sleep(1)
    # Load the policies
    policyA = Policy(
        name="Signals Access Policy", path="EXAMPLES/policy_signals_access.pl"
    )
    policyB = Policy(
        name="Vehicle Ownership Policy", path="EXAMPLES/policy_vehicle_ownership.pl"
    )
    ngac.load_policy(policyA.path, token="admin_token")
    ngac.load_policy(policyB.path, token="admin_token")
    policies = [policyA, policyB]
    target_policy = Policy(name="target_policy")
    ngac.combine_policies(policies, target_policy, token="admin_token")
    assert ngac.switch_to(target_policy, token="admin_token").status_code == 200
    print(ngac.get_policy(token="admin_token").text)
    assert True


def test_load_policy():
    """
    Test loading a policy from file
    """
    if os.getcwd().endswith("src"):
        from NGAC.ngac import NGAC
        from NGAC.ngac_types.ngac_policy import Policy
        from NGAC.ngac_types.user import User
        from NGAC.ngac_types.resource import Resource
    else:
        from ngac import NGAC
        from ngac_types.ngac_policy import Policy
        from ngac_types.user import User
        from ngac_types.resource import Resource
    ngac = NGAC()
    import time

    policy = Policy(name="CondPolicy1", path="./EXAMPLES/condpolicy1.pl")
    time.sleep(2)
    # Switch to the policy
    print(ngac.switch_to(policy, token="admin_token").text)
    print(ngac.get(Policy, token="admin_token").text)


def test_set_get_policy():
    """
    Test the ability to set and get policies
    """
    import time

    if os.getcwd().endswith("src"):
        from NGAC.ngac import NGAC
        from NGAC.ngac_types.ngac_policy import Policy
        from NGAC.ngac_types.user import User
        from NGAC.ngac_types.resource import Resource
    else:
        from ngac import NGAC
        from ngac_types.ngac_policy import Policy
        from ngac_types.user import User
        from ngac_types.resource import Resource
    ngac = NGAC()
    time.sleep(2)

    print(ngac.switch_to(Policy(name="Policy (b)"), token="admin_token").text)
    assert ngac.get(Policy, token="admin_token").text.split("\n")[0] == "Policy (b)"
    print(ngac.switch_to(Policy(name="Policy (a)"), token="admin_token").text)
    assert ngac.get(Policy, token="admin_token").text.split("\n")[0] == "Policy (a)"


def test_ngac_server():
    """
    Tests the NGAC server against the test cases
    defined in the tog-ngac repository
    """
    return
    import os
    import subprocess
    import time

    def call_ngac():

        # Get all the tests in the test folder and run them

        # Get the correct path to the test folder
        possible_paths = [("src", "./NGAC/TEST"), ("NGAC", "./TEST")]
        test_path = ""
        for path in possible_paths:
            if os.getcwd().endswith(path[0]):
                test_path = path[1]
                break
        if test_path == "":
            raise Exception("Could not find test folder")
        tests = os.listdir(f"{test_path}")
        for test in tests:
            if test.endswith(".sh"):
                print("-" * 40)
                print(f"Running test {test}")
                print("-" * 40)
                print(f"{test_path}/{test}")
                subprocess.run([f"{test_path}/{test}"], shell=True)

    with NGAC() as ngac:
        time.sleep(2)
        call_ngac()
    # Go over all of the logs and check if there are any errors
    path = (
        "./NGAC/executables/LOG" if os.getcwd().endswith("src") else "./executables/LOG"
    )
    files = os.listdir(path)
    files.sort()
    print("-" * 40)
    print(f"Latest log file: {files[-1]}")
    print("-" * 40)
    found = False
    for file in files:
        if file.endswith(".log"):
            print(f"Opening {file}")
            with open(f"{path}/{file}", "r") as f:
                if "ERROR" in f.read():
                    print(f"Error in {file}")
                    found = True
                    assert False
            print("-" * 40)
    if not found:
        print("No errors found")
    else:
        print("Errors found")
        assert False
    subprocess.run(["rm", "-r", f"{path}"])


def get_all_tests():
    """
    Returns all tests in the file

    [(function_name,function),...]
    """
    d = globals()
    tests = []
    for name in d:
        if name.startswith("test_"):
            tests.append((name, globals()[name]))
    return tests


def parse_args():
    """
    Parse the command line arguments
    """
    import argparse

    args = argparse.ArgumentParser(
        description="Test the NGAC server in a standalone fashion",
    )
    args.add_argument(
        "--test",
        type=str,
        default="add_get_policy",
        help="The test to run. If not specified, all tests will be run",
        required=False,
    )
    args.add_argument(
        "--info",
        type=str,
        default="",
        help="""Print info about the program,
        such as the tests that are available""",
        action="store",
        required=False,
    )

    return args.parse_args()


def test_access():
    """
    Combines 2 policies and makes 2 access requests,
    the first should pass, the second should fail
    """
    if os.getcwd().endswith("src"):
        from NGAC.ngac import NGAC
        from NGAC.ngac_types.ngac_policy import Policy
        from NGAC.ngac_types.user import User
        from NGAC.ngac_types.resource import Resource
    else:
        from ngac import NGAC
        from ngac_types.ngac_policy import Policy
        from ngac_types.user import User
        from ngac_types.resource import Resource
    import time

    ngac = NGAC()
    time.sleep(2)
    # Default policy is none
    SignalAccessPolicy = Policy(
        name="Signals Access Policy", path="EXAMPLES/policy_signals_access.pl"
    )
    VehicleOwnershipPolicy = Policy(
        name="Vehicle Ownership Policy", path="EXAMPLES/policy_vehicle_ownership.pl"
    )
    CombinedPolicy = Policy(name="Combined Policy")

    # Ensure that the default policy is none
    ret = ngac.get(Policy, token="admin_token").text
    if "none" not in ret:
        ret = ngac.switch_to(Policy(name="none"), token="admin_token")
    ret = ngac.get(Policy, token="admin_token").text

    assert "none" in ret

    # Load the two policies
    ret = ngac.load(SignalAccessPolicy, token="admin_token").status_code

    assert ret == 200

    ret = ngac.load(VehicleOwnershipPolicy, token="admin_token").status_code
    assert ret == 200

    # Combine the two policies
    assert (
        ngac.combine_policies(
            [SignalAccessPolicy, VehicleOwnershipPolicy],
            CombinedPolicy,
            token="admin_token",
        ).status_code
        == 200
    )

    # Switch to the combined policy
    assert ngac.switch_to(CombinedPolicy, token="admin_token").status_code == 200

    # Check that the combined policy is the current policy
    ret = ngac.get(Policy, token="admin_token").text
    assert "Combined Policy" in ret

    access_request = (
        User(id="Sebastian", attributes=[]),
        "r",
        Resource(id="VIN-1001 Door Signals"),
    )

    # Check that the access request is allowed
    assert ngac.validate(
        access_request,
        token="admin_token",
    )

    # Failcase: Check that the access request is denied
    access_request = (
        User(id="Aebastian", attributes=[]),
        "w",
        Resource(id="VIN-1001 Door Signals"),
    )
    assert not ngac.validate(
        access_request,
        token="admin_token",
    )


if __name__ == "__main__":

    if os.getcwd().endswith("src"):
        from NGAC.info import *
    else:
        from info import *
    test_access()
    pass
    # Parse the command line arguments
    args = parse_args()

    import sys

    test_load_policy()

    # Set the exception hook, very important for the tests

    # Get all available tests
    tests = get_all_tests()

    # If the user wants to print info about the tests then do so
    if args.info != "":
        if args.info == "tests":
            # Highlight the rubric in dark green
            print("\033[32m" + "Tests:" + "\033[0m")
            for test_name, test_function in get_all_tests():
                # Highlights description in bright yellow and the name in dark yellow
                print(
                    "\033[33m"
                    + f"{test_name}:"
                    + "\033[0m"
                    + "\033[93m"
                    + f"\t{test_function.__doc__}"
                    + "\033[0m"
                )
            exit(0)

    # Now the user wants to run a test
    print("-" * 80)
    info(InfoTypes(), "Running tests")
    info(Info(), f"Tests: {args.test}")
    info(Info(), f"Tests available: {[name for name, _ in tests]}")
    print("-" * 80)

    # If the user wants to run all tests, then do so
    if args.test == "all" or args.test == "":
        for test_name, test_function in tests:

            print("*" * 50)
            print(f"Running test {test_name}")
            print("*" * 50)
            test_function()
            print(" " * 22 + "! OK !")
    else:
        # The user wants to run a specific test
        for test_name, test_function in tests:
            # Look for the test
            if test_name == args.test:

                print("*" * 50)
                print(f"Running test {test_name}")
                print("*" * 50)
                # Run the test
                test_function()
                print(" " * 22 + "! OK !")
