"""
    Here we can test the entire application.
"""

from tests.tests import *
from NGAC.executables.ngac_server import *
from NGAC.executables.exec_runner import *
from NGAC.executables.cme import *
from NGAC.executables.pep import *


class TestClass:
    def test_method(self):
        """
        This is a test method, it is not testing anything.
        """
        assert 1 == 1
