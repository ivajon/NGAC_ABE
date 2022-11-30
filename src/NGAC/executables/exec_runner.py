"""
ExecRunner
---

An abstraction for starting executables in a "platform agnostic" manner.
"""

import subprocess
import os


def get_extension(os_name):
    """
    Gets the extension for the executable based on the OS name.
    """
    if os_name == "posix":
        return ""
    elif os_name == "mac":
        return ".app"  # Not sure if this is correct
    else:
        raise Exception("Unsupported OS")


class ExecRunner:
    """
    ExecRunner
    ---

    This is a class should not be used in a standalone manner.
    """

    def __init__(
        self, path, args, logger="tee", log_folder="./LOG", log_name=""
    ) -> None:
        """
        Initialize the ExecRunner class.
        """
        self.path = path
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
        Starts the executable.
        """

        self.pid = subprocess.Popen(
            [self.path, self.args],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
        )

        self.logger = subprocess.Popen(
            [self.logger_app, self.log_name],
            stdin=self.pid.stdout,
            stdout=subprocess.PIPE,
        )
        self.pid.stdout.close()

        self.err_logger = subprocess.Popen(
            [self.logger_app, f".{self.log_name.strip('.txt')}_err.txt"],
            stdin=self.pid.stderr,
            stdout=subprocess.PIPE,
        )
        self.pid.stderr.close()

        self.is_running = True

    def stop(self):
        """
        Stop the executable.
        """
        kill_process(self.pid, self.path)
        kill_process(self.logger, self.path)
        self.is_running = False

    def __enter__(self):
        """
        Called when the class is used in a with statement.
        """
        self.start()
        return self

    def __exit__(self, _exc_type, _exc_value, _traceback):
        """
        Called when the class is used in a with statement.
        """
        self.stop()

    def name(self):
        """
        Get the name of the executable.
        """
        return self.path.split("/")[-1].strip(".exe")


def kill_process(p: subprocess.Popen, name=""):
    """
    Kills a process, quite violently if needed
    """
    # Be kind
    p.terminate()
    p.wait()
    pid = p.pid
    p.terminate()

    try:
        # Be cruel
        if "python" in name:
            raise Exception("Python process killed")
        p.kill()
        os.kill(pid, 0)
        # If the process is still running, kill it
        if p.poll() is None:
            subprocess.call(["kill", "-9", str(pid)])
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
