# Standalone executables for NGAC

This folder contains standalone executables for NGAC.

To run the executables, you need to have [SWI-Prolog](https://www.swi-prolog.org/).

To run the executables as a python package you also need to have [python](https://www.python.org/) installed.

## Executables

- [NGAC server](./ngac_server) or [ngac_server.exe](./ngac_server.exe)
- [PEP](./pep) or [pep.exe](./pep.exe)
- [PDP](./pdp) or [pdp.exe](./pdp.exe)

## Python package

Simple wrappers for the executables are provided in this folder. It runs the executables as subprocesses and terminates them when the python process is terminated.

This makes managing the executables easier, as you don't have to worry about terminating them. Moreover, it allows you to execute this package as a subprocess, and run the servers in the background.

The files that exist in this folder are:

- [ngac_server.py](./ngac_server.py)
- [pep.py](./pep.py)
- [pdp.py](./pdp.py)
- [main.py](./__main__.py)
- [init.py](./__init__.py)

## Usage

```python

import subprocess

pid = subprocess.Popen(["python", "-m", "executables"])

# do something, like sending requests to the servers
pid.kill()
```
