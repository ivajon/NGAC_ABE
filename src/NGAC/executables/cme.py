import os

from exec_runner import ExecRunner


class CME(ExecRunner):
    def __init__(self, path="./cme", args="") -> None:
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
