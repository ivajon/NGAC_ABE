
class InfoTypes:
    def get_start(self) -> str:
        """
        Returns the color prefix
        """
        # Basic info is in grey
        return "\033[90m"

    def get_end(self) -> str:
        """
        Returns the color postfix
        """
        # Basic info is in grey
        return "\033[0m"


class Error(InfoTypes):
    def get_start(self) -> str:
        return "\033[91m"

    def get_end(self) -> str:
        return "\033[0m"


class Info(InfoTypes):
    def get_start(self) -> str:
        # Info messages are blue
        return "\033[94m"

    def get_end(self) -> str:
        return "\033[0m"


class Success(InfoTypes):
    def get_start(self) -> str:
        # Success messages are green
        return "\033[92m"

    def get_end(self) -> str:
        return "\033[0m"


class Channel:
    def t():
        """
        Returns the type of the channel
        """
        return Channel


class StdOut(Channel):
    def t():
        """
        Returns the type of the channel
        """
        return StdOut


class File(Channel):
    """
    Write to a file, creating it if it doesn't exist, since we are logging to file
    it does not support colors

    :param path: Path to the file

    Uses wa+ mode, so the file is created if it doesn't exist, and the file is
    opened for writing at then end of the file.
    """

    def __init__(self, path):
        self.path = path

    def t(self):
        """
        Returns the type of the channel
        """
        return File


class StdErr(Channel):
    def t():
        """
        Returns the type of the channel
        """
        return StdErr


def print_color(color, message):
    """
    Prints a message in a specific color

    :param color: The color specified by its rgb values
    :param message: The message to print

    :return: None
    """
    print(f"\033[38;2;{color[0]};{color[1]};{color[2]}m{message}\033[0m")


def info(t: InfoTypes, msg: str, channel: Channel = StdOut) -> None:
    import sys

    """
    Prints a message to the console

    :param t: The type of message
    :param msg: The message to print
    :param channel: The channel to print to

    :return: None

    ```python
    from info import info, Info, Error, Success
    info(Info(), "This is an info message")
    info(Error(), "This is an error message")
    info(Success(), "This is a success message")
    ```

    Logging to a file:
    ```python
    from info import info, Info, Error, Success, File
    info(Info(), "This is an info message", File("log.txt"))
    info(Error(), "This is an error message", File("log.txt"))
    info(Success(), "This is a success message", File("log.txt"))
    ```
    """
    if channel.t() == File:
        with open(channel.path, "a+") as f:
            f.write(f"{type(t).__name__}:\n\t{msg}")
    elif channel.t() == StdOut:
        print(
            f"{t.get_start()}{type(t).__name__}:\n\t{msg}{t.get_end()}", file=sys.stdout
        )
    elif channel.t() == StdErr:

        print(
            f"{t.get_start()}{type(t).__name__}:\n\t{msg}{t.get_end()}", file=sys.stderr
        )
    else:
        raise Exception("Invalid channel type")


def test_info():
    info(Info(), "This is an info message")
    info(Error(), "This is an error message")
    info(Success(), "This is a success message")
    info(Info(), "This is an info message", File("log.txt"))
    info(Error(), "This is an error message", File("log.txt"))
    info(Success(), "This is a success message", File("log.txt"))
    info(Info(), "This is an info message", StdErr)
    info(Error(), "This is an error message", StdErr)
    info(Success(), "This is a success message", StdErr)


def test_print_color():
    print_color((255, 0, 0), "This is red")
    print_color((0, 255, 0), "This is green")
    print_color((0, 0, 255), "This is blue")
    print_color((255, 255, 255), "This is white")
    print_color((0, 0, 0), "This is black")
