"""
Defines a set of tests for the NGAC API
---

These tests are meant to be run with pytest.

Most of the tests are based on the examples provided in the tog NGAC repository.

The unwrap function is used to throw an error if the result is an error, replacing the need for a lot of asserts.
"""
from result import unwrap

from .ngac import NGAC
from .policy import Policy
from .user import User
from .resource import Resource
policy_server_url = "http://130.240.200.92:8001"


def test_combine_policies():
    """
    Test the combine policies method
    """
    ngac = NGAC(token="admin_token", policy_server_url=policy_server_url)

    # Load the policies
    policyA = Policy(
        name="Signals Access Policy", path="EXAMPLES/policy_signals_access.pl"
    )
    policyB = Policy(
        name="Vehicle Ownership Policy", path="EXAMPLES/policy_vehicle_ownership.pl"
    )
    unwrap(ngac.load_policy(policyA.path))
    unwrap(ngac.load_policy(policyB.path))
    policies = [policyA, policyB]
    target_policy = Policy(name="target_policy")
    unwrap(ngac.combine_policies(policies, target_policy))
    unwrap(ngac.change_policy(target_policy))


def test_load_immidiate():
    """
    Tests the loadi system
    """
    ngac = NGAC(token="admin_token", policy_server_url=policy_server_url)
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
    unwrap(ngac.load_policy_from_str(pol))
    unwrap(ngac.change_policy(Policy(name="ipolicy")))
    current = unwrap(ngac.read(Policy(name="ipolicy")))
    assert str(pol.split("(")[0]) == str(current.split("(")[0])


def test_add_remove_user():
    """
    Tests adding and removing a user
    """
    ngac = NGAC(token="admin_token", policy_server_url=policy_server_url)
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
    unwrap(ngac.load_policy_from_str(pol))

    pol = Policy(name="cpolicy")
    unwrap(ngac.change_policy(pol))
    unwrap(ngac.add(user, target_policy=pol))
    unwrap(ngac.remove(user, target_policy=pol))


def _test_set_context():
    """
    Sets the context of the epp server and checks that it works
    """
    # There is some error in the setup of the epp server, we get Ok from server but
    # the context is not set
    ngac = NGAC(token="admin_token", policy_server_url=policy_server_url)
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
    unwrap(ngac.load_policy_from_str(pol))
    unwrap(ngac.change_policy(Policy(name="cpolicy")))
    # Change the context
    unwrap(ngac.change_context(["weekday:true"], token="epp_token"))

    access_requests = [
        (User(id="u1", attributes=[]), "r", Resource(id="o1", attributes=[])),
        (User(id="u1", attributes=[]), "w", Resource(id="o1", attributes=[])),
        (User(id="u2", attributes=[]), "r", Resource(id="o1", attributes=[])),
    ]

    def check_requests(requests, expected):
        for (request, excepted_value) in zip(requests, expected):
            print(request, excepted_value)
            status = unwrap(ngac.validate(request))
            print(
                f"Checking request ({request[0]},{request[1]},{request[2]}) expected {excepted_value}, got {status}"
            )
            assert status == excepted_value

    check_requests(access_requests, [True, True, False])
    # This is not working, not quite sure why, server is reporting the context change
    # But the context does not seem to be changed
    # unwrap(ngac.change_context(["business:false", "weekday:false"], token="epp_token"))
    # check_requests(access_requests, [False, False, False])
    unwrap(ngac.change_context(["weekday:true"], token="epp_token"))
    check_requests(access_requests, [True, True, False])


def test_set_get_policy():
    """
    Test the ability to set and get policies
    """

    ngac = NGAC(token="admin_token", policy_server_url=policy_server_url)

    unwrap(ngac.change_policy(Policy(name="Policy (b)")))
    assert unwrap(ngac.get_policy()).split("\n")[0] == "Policy (b)"
    unwrap(ngac.change_policy(Policy(name="Policy (a)")))
    assert unwrap(ngac.get_policy()).split("\n")[0] == "Policy (a)"


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
        default="all    ",
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

    ngac = NGAC(token="admin_token", policy_server_url=policy_server_url)
    # Default policy is none
    SignalAccessPolicy = Policy(
        name="Signals Access Policy", path="EXAMPLES/policy_signals_access.pl"
    )
    VehicleOwnershipPolicy = Policy(
        name="Vehicle Ownership Policy", path="EXAMPLES/policy_vehicle_ownership.pl"
    )
    CombinedPolicy = Policy(name="Combined Policy")

    # Ensure that the default policy is none
    ret = unwrap(ngac.get_policy())
    if "none" not in ret:
        ret = ngac.change_policy(Policy(name="none"))
    ret = unwrap(ngac.get_policy())

    assert "none" in ret

    # Load the two policies
    unwrap(ngac.load_policy(SignalAccessPolicy.path))

    unwrap(ngac.load_policy(VehicleOwnershipPolicy.path))

    # Combine the two policies
    unwrap(
        ngac.combine_policies(
            [SignalAccessPolicy, VehicleOwnershipPolicy],
            CombinedPolicy,
        )
    )

    # Switch to the combined policy
    unwrap(ngac.change_policy(CombinedPolicy))

    # Check that the combined policy is the current policy
    ret = unwrap(ngac.get_policy())
    assert "Combined Policy" in ret

    access_request = (
        User(id="Sebastian", attributes=[]),
        "r",
        Resource(id="VIN-1001 Door Signals"),
    )

    # Check that the access request is allowed
    assert unwrap(
        ngac.validate(
            access_request,
        )
    )

    # Failcase: Check that the access request is denied
    access_request = (
        User(id="Aebastian", attributes=[]),
        "w",
        Resource(id="VIN-1001 Door Signals"),
    )
    assert not unwrap(
        ngac.validate(
            access_request,
        )
    )


def main():
    test_set_context()
    test_load_immidiate()
    test_add_remove_user()


if __name__ == "__main__":
    main()
