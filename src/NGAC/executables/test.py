"""
Test the Executables

This module is ran standalone so the tests should be ran in a standalone fashion
"""

from exec_runner import *
from ngac_server import *
from pep import *

# Run all functions with the prefix "test_" in this module

if __name__ == "__main__":
    import inspect
    import sys

    # Get all functions in this module
    functions = inspect.getmembers(sys.modules[__name__], inspect.isfunction)
    print(functions)
    # Run all functions with the prefix "test_"
    for function in functions:
        if function[0].startswith("test_"):
            print(f"Running {function[0]}")
            function[1]()
