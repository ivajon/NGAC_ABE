"""
Info
---

Different types of info need different colors in the terminal.


"""


class InfoTypes:
    """
    Generic `info` message, these are grey
    """

    def get_start(self) -> str:
        """
        Returns the color prefix
        """
        return "\033[90m"

    def get_end(self) -> str:
        """
        Returns the color postfix
        """
        return "\033[0m"


class Error(InfoTypes):
    """
    Specifies that the message is an `error` message, these are red.
    """

    def get_start(self) -> str:
        return "\033[91m"

    def get_end(self) -> str:
        return "\033[0m"


class Info(InfoTypes):
    """
    Specifies that the message is an `info` message, these are blue.
    """

    def get_start(self) -> str:
        return "\033[94m"

    def get_end(self) -> str:
        return "\033[0m"


class Success(InfoTypes):
    """
    Specifies that is it a `success` message, these are green.
    """

    def get_start(self) -> str:
        return "\033[92m"

    def get_end(self) -> str:
        return "\033[0m"


class Channel:
    """
    Generic channel, this can not be printed to.
    """

    def t():
        """
        Returns the type of the channel
        """
        return Channel


class StdOut(Channel):
    """
    Specifies that the output channel should be `stdout`.
    """

    def t():
        """
        Returns the type of the channel
        """
        return StdOut


class File(Channel):
    """
    Specifies that the output channel should be a `file`.
    """

    def __init__(self, path):
        self.path = path

    def t(self):
        """
        Returns the type of the channel
        """
        return File


class StdErr(Channel):
    """
    Specifies that the output channel should be `stderr`.
    """

    def t():
        """
        Returns the type of the channel
        """
        return StdErr


def print_color(color, message):
    """
    Prints the [`message`] in the specified [`color`]
    """
    print(f"\033[38;2;{color[0]};{color[1]};{color[2]}m{message}\033[0m")


def info(message_type: InfoTypes, message: str, channel: Channel = StdOut):
    """
    Logs a [`message_type`] [`message`] to the [`channel`] specified
    """
    import sys

    if channel.t() == File:
        with open(channel.path, "a+") as f:
            f.write(f"{type(message_type).__name__}:\n\t{message}")
    elif channel.t() == StdOut:
        print(
            f"{message_type.get_start()}{type(message_type).__name__}:\n\t{message}{message_type.get_end()}",
            file=sys.stdout,
        )
    elif channel.t() == StdErr:

        print(
            f"{message_type.get_start()}{type(message_type).__name__}:\n\t{message}{message_type.get_end()}",
            file=sys.stderr,
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
