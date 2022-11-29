"""
CME
---

This module contains the CME class, which is used to start and stop the CME executable.

The CME executable is used to manage the NGAC database. It is used to add, remove, and modify policies, attributes, and resources.

Usage:
```python

    cme = CME()
    cme.start()
    # Do stuff
    cme.stop()

    # Or use the with statement
    with CME() as cme:
        # Do stuff
```
"""
from exec_runner import ExecRunner


class CME(ExecRunner):
    def __init__(self, path="cme", args="") -> None:
        """
        Initialize the CME class

        :param path: Path to the CME executable
        :param args: Arguments to pass to the CME executable
        """
        self.path = path
        self.args = args
        super().__init__(path, args)


def test_cme():
    cme = CME()
    cme.start()
    # Try to connect to the CME
    import subprocess
    import time

    time.sleep(1)
    cme.stop()

if __name__ == "__main__":
    cme = CME()
    cme.start()
    while True:
        pass