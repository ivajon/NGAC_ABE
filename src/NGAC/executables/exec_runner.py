"""
ExecRunner
---

This class is used to start and stop executables
it is used to start and stop all of the NGAC executables.

## Usage

```python
python = ExecRunner("python", "-c 'import time;while True:print(\"Hello world\");time.sleep(1)'") 
with python:
    assert python.is_running == True
assert python.is_running == False
```
"""

import subprocess
import os
from typing import Literal
from sys import platform


def get_extension(os_name):
    """
    Gets the extension for the executable based on the OS name
    """
    if os_name == "nt":
        return ".exe"
    elif os_name == "posix":
        return ""
    elif os_name == "mac":
        return ""
    else:
        raise Exception("Unsupported OS")


class ExecRunner:
    logger = None
    """
      Logs the output of the `executable` to a file
    """

    err_logger = None
    """
      Logger that logs the error output of the executable
    """
    executable = None
    """
      Main app that will be ran as subprocess
    """

    def __init__(
        self, file_name, args, logger="tee", log_folder="./LOG", log_name=""
    ) -> None:
        """
        Initialize the ExecRunner class
        """

        def get_os_name(os_name) -> Literal["windows", "arch", "linux", "macos"]:
            print(os_name)
            print(platform)

            if platform == "win32" or platform == "win64":
                return "windows"
            elif platform == "darwin":
                return "macos"
            elif platform == "linux" or platform == "linux2" or os.name == "posix":
                # Check if we are on arch, ubuntu, mac, etc
                if os.path.exists("/etc/arch-release"):
                    return "arch"
                elif os.path.exists("/etc/debian_version"):
                    return "linux"
                else:
                    return "linux"
            else:
                raise Exception("Unsupported OS")

        # We need to know the runnable file extension for the OS
        # If we are on windows, append .exe to the path
        self.path = (# If we are in executables don't add prefix executables, otherwise add it
            ("" if file_name.startswith("executables") else "executables/")+
            "./" + get_os_name(os.name) + "/" + file_name + get_extension(os.name)
        )
        self.path += get_extension(os.name)
        self.args = args
        self.is_running = False
        self.logger_app = logger
        self.log_name = log_name
        if self.log_name == "":
            self.log_name = f"{log_folder}/{self.name()}_log.txt"
        # Create the folders if needed
        if not os.path.exists(log_folder):
            os.makedirs(log_folder)

    def start(self):
        """
        Start the executable
        """
        # Start the executable, passing its stdout to a file and stderr to the console
        self.executable = subprocess.Popen(
            [self.path, self.args],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            preexec_fn=os.setsid,
            shell=True,
        )
        # Read one line at a time from the executable
        for i in [0,1,2]:
            print(self.executable.stdout.readline())
        # Capture the output of the executable for a bit and ensure that it is running
        self.is_running = self.executable.poll() is None

        # Start the logger
        self.logger = subprocess.Popen(
            [self.logger_app, self.log_name],
            stdin=self.executable.stdout,
            stdout=subprocess.PIPE,
            preexec_fn=os.setsid,
        )
        self.executable.stdout.close()

        self.err_logger = subprocess.Popen(
            [self.logger_app, f".{self.log_name.strip('.txt')}_err.txt"],
            stdin=self.executable.stderr,
            stdout=subprocess.PIPE,
            preexec_fn=os.setsid,
        )
        # Check if the executable is still running
        is_running = lambda self, p: self.is_running and (p.poll() is None)
        self.executable.stderr.close()

        # Check that the process is still running
        self.is_running = is_running(self, self.executable)
        self.is_running = is_running(self, self.logger)
        self.is_running = is_running(self, self.err_logger)

        self.is_running = True

    def stop(self):
        """
        Stop the executable
        """
        import signal

        # Kill all the processes
        try:
            os.killpg(os.getpgid(self.executable.pid), signal.SIGTERM)
        except ProcessLookupError:
            print("Process not found")
        try:
            os.killpg(os.getpgid(self.logger.pid), signal.SIGTERM)
        except ProcessLookupError:
            print("Process not found")
        try:
            os.killpg(os.getpgid(self.err_logger.pid), signal.SIGTERM)
        except ProcessLookupError:
            print("Process not found")
        print(f"Stopped {self.name()}")
        # Check if the executable is still running
        is_running = lambda self, p: self.is_running and (p.poll() is None)

        # Check that the process is no longer running
        self.is_running = is_running(self, self.executable)
        self.is_running = is_running(self, self.logger)
        self.is_running = is_running(self, self.err_logger)

    def __enter__(self):
        """
        Called when the class is used in a with statement
        """
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Called when the class is used in a with statement
        """
        self.stop()

    def name(self):
        """
        Get the name of the executable
        """
        return self.path.split("/")[-1].strip(".exe")

    def __str__(self):
        """
        Called when the class is printed
        """
        return f"{self.name()}({self.path})"

    def __repr__(self):
        """
        Called when the class is printed
        """
        return str(self)


def kill_process(p: subprocess.Popen, name=""):
    """
    Kills a process, quite violently if needed
    """
    # Be kind
    p.terminate()
    p.wait()
    executable = p.executable
    p.terminate()
    try:
        # Be cruel
        if "python" in name:
            raise Exception("Python process killed")
        # p.kill()
        os.kill(executable, 0)
        # If the process is still running, kill it
        if p.poll() is None:
            subprocess.call(["kill", "-9", str(executable)])
        p.wait()
    except (OSError, subprocess.CalledProcessError):
        os._exit(0)
    except Exception as e:
        pass


def test_start_stop():
    """
    Tests starting and stopping an executable
    """
    python = ExecRunner(
        "python", "-c 'import time;while True:print(\"Hello world\");time.sleep(1)'"
    )
    with python:
        assert python.is_running == True
    assert python.is_running == False


def test_with_explicit_start_stop():
    """
    Tests starting and stopping an executable
    """
    python = ExecRunner(
        "python", "-c 'import time;while True:print(\"Hello world\");time.sleep(1)'"
    )
    python.start()
    assert python.is_running == True
    python.stop()
    assert python.is_running == False
