"""
Next Generation Access Control (NGAC) server
---

This file contains functionality to run the NGAC server as a standalone application.

## Usage
```bash
    python .
```
"""
from server_runner import NGAC


if __name__ == "__main__":
    ngac = NGAC()
    """
    Starts the ngac servers
    """
    with ngac:
        print("NGAC started")
        while True:
            pass
    print("NGAC stopped")
