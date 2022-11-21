"""
Next Generation Access Control (NGAC) server
---

This is the main server for the NGAC application. It is responsible for handling all the requests from the clients.

All interaction with the server is done using http requests. The server files are defined in the NGAC/executables directory.
And are compiled from the [tog-ngac-cross-cpp](https://github.com/tog-rtd/tog-ngac-crosscpp) source code.

## Abstraction api

- Creating a new ngac instance `ngac_server = NGACServer()`
- Starting the server `ngac_server.start()`
- Stopping the server `ngac_server.stop()`
- Checking if the server is running `ngac_server.is_running`

### Notes

#### Subprocesses
The server is started in a separate thread, so it is non-blocking. This means that the server will not block the main thread.
This also infers that the server will not halt if the main thread is halted. This is a problem with running everything as sub processes.
The solution is to manually kill the server process when the main thread is halted.

#### Side effects of starting the NGAC server
When starting the NGAC server, the server will automatically start the CME and PEP servers. This is done to make the NGAC server
easier to use. The CME and PEP servers are started in the background, and are not accessible to the user. This is done to prevent
the user from accidentally stopping the CME or PEP servers. The CME and PEP servers are stopped when the NGAC server is stopped.

## Usage
```python
    ngac_server = NGACServer()
    ngac_server.start()
    # Do stuff
    ngac_server.stop()


    # Or use the with statement
    with NGACServer() as ngac_server:
        # Do stuff
```

"""

import os

from .exec_runner import ExecRunner


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
    print("Ngac server is running: ", ngac_server.is_running)
    assert ngac_server.is_running
    print("Ngac server is running: ", ngac_server.is_running)
    ngac_server.stop()
    assert ngac_server.is_running == False
    print("Ngac server is running: ", ngac_server.is_running)


if __name__ == "__main__":
    test_ngac_server()
