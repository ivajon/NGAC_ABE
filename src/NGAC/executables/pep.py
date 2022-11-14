import os

from exec_runner import ExecRunner


class PEP(ExecRunner):
    def __init__(self, path="./pep_server", args="") -> None:
        """
        Initialize the PEP class

        :param path: Path to the PEP executable
        :param args: Arguments to pass to the PEP executable
        """
        self.path = path
        self.args = args
        super().__init__(path, args)


def test_pep():
    with PEP() as p:
        print(p.is_running)
        # Do stuff
        # pep.stop() is called automatically
        assert p.is_running == False


if __name__ == "__main__":
    test_pep()
