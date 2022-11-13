"""
Defines test cases for the user class
"""


def relative_import(package, module):
    """
    Solves pythons relative import problem
    """
    import os

    exec(
        f"""from {"" if os.getcwd().endswith("ngac_types") else "ngac_types." if os.getcwd().endswith("NGAC") else "NGAC.ngac_types."}{package} import {module}"""
    )
    return locals()[module]


UserAttribute = relative_import("ngac_attribute", "UserAttribute")
User = relative_import("user", "User")


def test_create_user():
    """
    Test user creation
    """
    user = User([], id="SomeUser")
    assert user.id == "SomeUser"


def test_create_with_attributes():
    """
    Test user creation with attributes
    """
    attributes = [
        UserAttribute("value1"),
        UserAttribute("value2"),
        UserAttribute("value3"),
    ]
    user = User(attributes, id="SomeUser")
    assert user.id == "SomeUser"
    assert user.get_attributes() == attributes


def test_list_like_user():
    """
    Test user class, list like operations
    """
    attributes = [
        UserAttribute("value1"),
        UserAttribute("value2"),
        UserAttribute("value3"),
    ]
    user = User(attributes, id="SomeUser")

    assert user[0] == attributes[0]
    assert user[1] == attributes[1]

    assert len(user) == 3
    popped = user.pop(0)
    assert popped == UserAttribute("value1")
    assert len(user) == 2
    user.push(UserAttribute("value4"))
    assert len(user) == 3
    assert user[2] == UserAttribute("value4")

    for attribute in user:
        assert attribute in attributes or attribute == UserAttribute("value4")


if __name__ == "__main__":
    test_create_user()
    test_create_with_attributes()
    test_list_like_user()
