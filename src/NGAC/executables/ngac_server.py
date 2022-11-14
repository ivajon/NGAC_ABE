import os

from exec_runner import ExecRunner


class NGACServer(ExecRunner):
    def __init__(self, path="./ngac_server", args="") -> None:
        """
        Initialize the CME class

        :param path: Path to the CME executable
        :param args: Arguments to pass to the CME executable
        """
        self.path = path
        self.args = args
        super().__init__(path, args)


def test_ngac_server():
    """
    Test the NGAC server
    """
    import time

    ngac_server = NGACServer()
    ngac_server.start()
    time.sleep(1)
    assert ngac_server.is_running()
    ngac_server.stop()
    assert not ngac_server.is_running()

if __name__ == "__main__":
    test_ngac_server()
