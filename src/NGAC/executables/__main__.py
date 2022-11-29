"""
Next Generation Access Control (NGAC) server
---

This file contains functionality to run the NGAC server as a standalone application.

## Usage
```bash
    python .
```
"""
from pep import PEP
from ngac_server import NGACServer
from cme import CME


class NGAC:
    """
    Next Generation Access Control (NGAC) server
    ---

    This is the main server for the NGAC application. It is responsible for handling all the requests from the clients.
    """

    def __init__(self: "NGAC") -> None:
        """
        Initialize the NGAC class
        """
        self.cme = CME()
        self.pep = PEP()
        self.ngac_server = NGACServer()

    def __enter__(self: "NGAC") -> "NGAC":
        """
        Enter the NGAC class
        """
        self.cme.start()
        self.pep.start()
        self.ngac_server.start()
        print("NGAC server started")
        return self

    def __exit__(self: "NGAC", exc_type, exc_value, traceback) -> None:
        """
        Exit the NGAC class
        """
        self.ngac_server.stop()
        self.cme.stop()
        self.pep.stop()
        print("NGAC server stopped")


if __name__ == "__main__":
    ngac = NGAC()
    """
    Ngac servers wrapper
    """
    print("NGAC created")

    print("Exception handler set")

    print("NGAC started")

    with ngac:
        print("NGAC started")
        for i in range(100000):
            pass
    print("NGAC stopped")
