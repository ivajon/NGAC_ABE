from pep import PEP
from ngac_server import NGACServer
from cme import CME


class NGAC:
    """
    Next Generation Access Control (NGAC) server.
    ---

    This is the main server for the NGAC application. It is responsible for handling all the requests from the clients.
    """

    def __init__(self: "NGAC") -> None:
        """
        Initialize the NGAC class.
        """
        self.cme = CME()
        self.pep = PEP()
        self.ngac_server = NGACServer()

    def start(self: "NGAC"):
        self.cme.start()
        self.pep.start()
        self.ngac_server.start()

    def stop(self: "NGAC"):
        self.ngac_server.stop()
        self.cme.stop()
        self.pep.stop()

    def __enter__(self: "NGAC") -> "NGAC":
        """
        Enter the NGAC class.
        """
        self.start()
        return self

    def __exit__(self: "NGAC", exc_type, exc_value, traceback) -> None:
        """
        Exit the NGAC class.
        """
        self.stop()
        print("NGAC server stopped")


def start() -> NGAC:
    ngac = NGAC()
    ngac.start()
    return ngac


def stop(ngac: NGAC):
    ngac.stop()


def test_servers():
    servers = NGAC()
    with servers:
        import time

        time.sleep(2)
        import requests

        url = "http://127.0.0.1:8001/paapi/setpol"
        args = {"policy": "Policy (a)", "token": "admin_token"}
        ret = requests.get(url, params=args)
        print(ret.text)
        assert ret.ok

if __name__ == "__main__":
    test_servers()
