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
    def __init__(self) -> None:
        """
        Initialize the NGAC class
        """
        self.cme = CME()
        self.pep = PEP()
        self.ngac_server = NGACServer()

    def __enter__(self):
        """
        Enter the NGAC class
        """
        self.cme.start()
        self.pep.start()
        self.ngac_server.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exit the NGAC class
        """
        self.ngac_server.stop()
        self.cme.stop()
        self.pep.stop()

    def __del__(self):
        """
        Delete the NGAC class
        """
        self.ngac_server.stop()
        self.cme.stop()
        self.pep.stop()



if __name__ == "__main__":
    ngac = NGAC()
    print("NGAC created")
    def panic_handler(*args):
        """
        Runs when the program is halted

        :param args: Arguments passed to the function

        Stops the servers.
        """
        ngac.__exit__(None, None, None)
        exit()
    import atexit
    atexit.register(panic_handler)
    import sys
    sys.excepthook = panic_handler
    print("Exception handler set")
    with ngac:
        print("NGAC started")
        while True:
            pass




