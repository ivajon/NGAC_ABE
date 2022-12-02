"""
Policy Enforcement Point (PEP)
---

This class wraps the `Tog-ngac-cross-cpp` executable and provides a pythonic interface to it.
The PEP is used to enforce policies on the system.

This file is not intended to be run directly, but rather ran as a part of the `ngac_server`.
"""
from exec_runner import ExecRunner


class PEP(ExecRunner):
    """
    PEP Sever python wrapper
    ---
    This class is used to start and stop the PEP server

    Usage:
    ```python
        pep = PEP()
        pep.start()
        # Do stuff
        pep.stop()

        # Or use the with statement
        with PEP() as pep:
            # Do stuff
    ```
    """

    def __init__(self, path="pep_server", args="") -> None:
        """
        Initialize the PEP class

        :param path: Path to the PEP executable
        :param args: Arguments to pass to the PEP executable
        """
        self.path = path
        self.args = args
        super().__init__(path, args)


def test_pep():
    p = PEP()
    with p:
        print(p.is_running)
        # Do stuff
        # pep.stop() is called automatically
    assert p.is_running == False


if __name__ == "__main__":
    test_pep()
