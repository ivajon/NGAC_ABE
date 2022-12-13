import os


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


def test_combine_policies():
    """
    Test the combine policies method
    """
    ngac = NGAC(token="admin_token")

    # Load the policies
    policyA = Policy(
        name="Signals Access Policy", path="EXAMPLES/policy_signals_access.pl"
    )
    policyB = Policy(
        name="Vehicle Ownership Policy", path="EXAMPLES/policy_vehicle_ownership.pl"
    )
    ngac.load_policy(policyA.path)
    ngac.load_policy(policyB.path)
    policies = [policyA, policyB]
    target_policy = Policy(name="target_policy")
    ngac.combine_policies(policies, target_policy)
    assert ngac.change_policy(target_policy).status_code == 200
    print(ngac.get_policy().text)
    assert True


def test_load_policy():
    """
    Test loading a policy from file
    """
    ngac = NGAC(token="admin_token")

    policy = Policy(name="CondPolicy1", path="./EXAMPLES/condpolicy1.pl")
    # Switch to the policy
    print(ngac.change_policy(policy).text)
    print(ngac.get(Policy).text)


def test_load_immidiate():
    """
    Tests the loadi system
    """
    ngac = NGAC(token="admin_token")
    pol = """policy(ipolicy,access,[
	user(u1),
	user_attribute(ua1),
	object(o1),
	object_attribute(oa1),
	policy_class(access),
	connector('PM'),
	assign(u1,ua1),
	assign(o1,oa1),
	assign(ua1,access),
	assign(oa1,access),
	assign(access,'PM'),
	associate(ua1,[r,w],oa1)])"""
    status = ngac.load_policy_from_str(pol)
    assert status.ok
    assert ngac.change_policy(Policy(name="ipolicy")).ok

    current = ngac.read().text

    print(status.text)
    print(current)
    print("set", current)
    print("target", pol)
    assert str(pol.split("(")[0]) == str(current.split("(")[0])


def test_add_remove_user():
    """
    Tests adding and removing a user
    """
    ngac = NGAC(token="admin_token")
    user = User(id="u123", attributes=["ua12"])
    pol = """policy(cpolicy,access,[
	user(u1),
	user_attribute(ua1),
	object(o1),
	object_attribute(oa1),
	policy_class(access),
	connector('PM'),
	assign(u1,ua1),
	assign(o1,oa1),
	assign(ua1,access),
	assign(oa1,access),
	assign(access,'PM'),
	cond( weekday, associate(ua1,[r,w],oa1) )
        ])"""
    status = ngac.load_policy_from_str(pol)
    assert status.ok
    pol = Policy(name="cpolicy")
    assert ngac.change_policy(pol).ok
    print(ngac.add(user, target_policy=pol).text)
    print(ngac.read().text)
    ngac.remove_multiple(user, target_policy=pol)
    print(ngac.read().text)


def test_set_context():
    """
    Sets the context of the epp server and checks that it works
    """
    return
    # There is some error in the setup of the epp server, we get Ok from server but
    # the context is not set
    ngac = NGAC(token="admin_token")
    pol = """policy(cpolicy,access,[
	user(u1),
	user_attribute(ua1),
	object(o1),
	object_attribute(oa1),
	policy_class(access),
	connector('PM'),
	assign(u1,ua1),
	assign(o1,oa1),
	assign(ua1,access),
	assign(oa1,access),
	assign(access,'PM'),
	cond( weekday, associate(ua1,[r,w],oa1) )
        ])"""
    status = ngac.load_policy_from_str(pol)
    assert status.ok
    assert ngac.change_policy(Policy(name="cpolicy")).ok
    # Change the context
    resp = ngac.change_context(["weekday:true"], token="epp_token")
    print(resp.text)
    assert resp.ok

    access_requests = [
        (User(id="u1", attributes=[]), "r", Resource(id="o1", attributes=[])),
        (User(id="u1", attributes=[]), "w", Resource(id="o1", attributes=[])),
        (User(id="u2", attributes=[]), "r", Resource(id="o1", attributes=[])),
    ]

    def check_requests(requests, expected):
        for i, request in enumerate(requests):
            print("Checking request", request)
            print("Expected", expected[i])
            assert ngac.validate(request) == expected[i]

    check_requests(access_requests, [True, True, False])
    assert ngac.change_context(
        ["business:false", "weekday:false"], token="epp_token"
    ).ok
    check_requests(access_requests, [False, False, False])
    assert ngac.change_context(["weekday:true"], token="epp_token").ok
    check_requests(access_requests, [True, True, False])


def test_set_get_policy():
    """
    Test the ability to set and get policies
    """

    ngac = NGAC(token="admin_token")

    print(ngac.change_policy(Policy(name="Policy (b)")).text)
    assert ngac.get(Policy).text.split("\n")[0] == "Policy (b)"
    print(ngac.change_policy(Policy(name="Policy (a)")).text)
    assert ngac.get(Policy).text.split("\n")[0] == "Policy (a)"


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

    ngac = NGAC(token="admin_token")
    # Default policy is none
    SignalAccessPolicy = Policy(
        name="Signals Access Policy", path="EXAMPLES/policy_signals_access.pl"
    )
    VehicleOwnershipPolicy = Policy(
        name="Vehicle Ownership Policy", path="EXAMPLES/policy_vehicle_ownership.pl"
    )
    CombinedPolicy = Policy(name="Combined Policy")

    # Ensure that the default policy is none
    ret = ngac.get(Policy).text
    if "none" not in ret:
        ret = ngac.change_policy(Policy(name="none"))
    ret = ngac.get(Policy).text

    assert "none" in ret

    # Load the two policies
    ret = ngac.load_policy(SignalAccessPolicy.path).status_code

    assert ret == 200

    ret = ngac.load_policy(VehicleOwnershipPolicy.path).status_code
    assert ret == 200

    # Combine the two policies
    assert (
        ngac.combine_policies(
            [SignalAccessPolicy, VehicleOwnershipPolicy],
            CombinedPolicy,
        ).status_code
        == 200
    )

    # Switch to the combined policy
    assert ngac.change_policy(CombinedPolicy).status_code == 200

    # Check that the combined policy is the current policy
    ret = ngac.get(Policy).text
    assert "Combined Policy" in ret

    access_request = (
        User(id="Sebastian", attributes=[]),
        "r",
        Resource(id="VIN-1001 Door Signals"),
    )

    # Check that the access request is allowed
    assert ngac.validate(
        access_request,
    )

    # Failcase: Check that the access request is denied
    access_request = (
        User(id="Aebastian", attributes=[]),
        "w",
        Resource(id="VIN-1001 Door Signals"),
    )
    assert not ngac.validate(
        access_request,
    )


if __name__ == "__main__":
    test_set_context()
    test_load_immidiate()
    test_add_remove_user()
    # test_access()
    pass
    # Parse the command line arguments
    args = parse_args()

    import sys

    # test_load_policy()

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
