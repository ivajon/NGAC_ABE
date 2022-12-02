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
When you start the NGAC server, you also need to start the CME and PEP servers. Look at the `start_ngac` function in the `__main__.py` file for an example of how to start the NGAC server.
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

from exec_runner import ExecRunner


class NGACServer(ExecRunner):
    def __init__(self, path="ngac_server", args="") -> None:
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
    log = ngac_server.start()
    print(log)
    assert log != [b"",b"",b""]
    time.sleep(1)
    print("Ngac server is running: ", ngac_server.is_running)
    assert ngac_server.is_running
    print("Ngac server is running: ", ngac_server.is_running)

    # Execute curl -s -G "http://127.0.0.1:8001/paapi/setpol" --data-urlencode "policy=Policy (a)" --data-urlencode "token=admin_token"
    # This should return a 200 status code

    import requests

    url = "http://127.0.0.1:8001/paapi/setpol"
    args = {"policy": "Policy (a)", "token": "admin_token"}
    ret = requests.get(url, params=args)
    print(ret.text)
    assert ret.ok
    ngac_server.stop()
    assert ngac_server.is_running == False


if __name__ == "__main__":
    test_ngac_server()
