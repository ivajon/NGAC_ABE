"""
    Here we can test the entire application.
"""
policy_server_url = "http://130.240.200.92:8001"
# from NGAC.test_ngac import *


def test_ngac_servers():
    from NgacApi.ngac import NGAC
    from result import unwrap
    from NgacApi.policy import Policy
    from NgacApi.user import User

    ngac = NGAC(token="admin_token", policy_server_url=policy_server_url)

    # Load a test policy
    pol = Policy(name="Signals Access Policy",
                 path="EXAMPLES/policy_signals_access.pl")
    print(ngac.load_policy(pol))

    # Swap to the policy
    print(ngac.change_policy(pol))

    # Create a user
    user = User(id="u1", attributes=["ua1"])
    print(ngac.add(user, pol.name))

    # Read the current policy
    print(ngac.get_policy())


if __name__ == "__main__":
    test_ngac_servers()
