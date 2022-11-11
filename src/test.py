"""
    Here we can test the entire application.
"""

from tests.tests import *


class TestClass:

    def test_ngac_attribute(self):
        """
        Test attribute class
        """
        from NGAC.ngac_types.ngac_attribute import Attribute

        attr = Attribute("SomeAttribute")

        assert attr.get_attr() == "SomeAttribute"

    def test_ngac_user(self):
        """
        Test user class
        """
        from NGAC.ngac_types.user import User
        from NGAC.ngac_types.ngac_attribute import UserAttribute as UA

        ua1 = UA("ua1")
        ua2 = UA("ua2")
        ua3 = UA("ua3")
        ua4 = UA("ua4")
        ua5 = UA("ua5")
        ua6 = UA("ua6")

        user = User([ua1, ua2, ua3, ua4], id="SomeUser")

        assert user.id == "SomeUser"
        assert user.get_attributes() == [ua1, ua2, ua3, ua4]

        user.append(ua5)
        assert user.get_attributes() == [ua1, ua2, ua3, ua4, ua5]

        user.remove(ua1)
        assert user.get_attributes() == [ua2, ua3, ua4, ua5]

        user.pop(0)
        assert user.get_attributes() == [ua3, ua4, ua5]

        user.push(ua6)
        assert user.get_attributes() == [ua3, ua4, ua5, ua6]

        truth = [ua3, ua4, ua5, ua6]
        for i, attr in enumerate(user):
            assert attr == truth[i]
