from typing import Callable
from functools import wraps
import sys
import os
import re

CURSOR_UP_ONE = "\x1b[1A"
ERASE_LINE = "\x1b[2K"

"""
[logging]
level = DEBUG
folder = logs
maxBytes = 10000000 

[NGAC]
policy = ipolicy.pl
# This admin_token should not be admin_token 
# in a production environment
admin_token = secrets/ngac_admin.key
url = http://130.240.200.92:8001

[ABE]
enabled = true      # enable ABE
url = http://31.208.238.201:59931


"""


class Cfg:
    cfg = {
        "logging": {"level": "DEBUG", "folder": "logs", "maxBytes": "10000000"},
        "NGAC": {
            "policy": "ipolicy.pl",
            "admin_token": "secrets/ngac_admin.key",
            "url": "http://130.240.200.92:8001",
        },
        "ABE": {"enabled": "true", "url": "http://31.208.238.201:59931"},
    }

    def __init__(self):
        pass

    def render(self) -> str:
        ret = "# Generated with the setup tool!\n\n"
        for key in self.cfg.keys():
            ret += f"[{key}]\n"
            for el in self.cfg[key].keys():
                ret += f"{el} = {self.cfg[key][el]}\n"
            ret += "\n"
        return ret

    def logging(self):
        return f"""
{var("level")}= {val(self.cfg["logging"]["level"])}
{var("folder")}= {val(self.cfg["logging"]["folder"])}
{var("maxBytes")}= {val(self.cfg["logging"]["maxBytes"])}
        """

    def NGAC(self):
        return f"""
{var("policy",l=15)}= {val(self.cfg["NGAC"]["policy"])}
{var("admin_token",l=15)}= {val(self.cfg["NGAC"]["admin_token"])}
{var("url",l=15)}= {val(self.cfg["NGAC"]["url"])}
    """

    def ABE(self):
        return f"""
{var("enabled")}= {val(self.cfg["ABE"]["enabled"])}
{var("url")}= {val(self.cfg["ABE"]["url"])}
        """


cfg = Cfg()


def color(color_, text):
    """
    Taken from https://stackabuse.com/how-to-print-colored-text-in-python/
    """
    num1 = str(color_)
    num2 = str(color_).ljust(3, " ")
    return f"\033[38;5;{num1}m{text}\033[0;0m"


def var(v, l=10):
    return f"{color(12,v)}" + " " * (l - len(v))


def val(v):
    return f"{color(3,v)}"


def heading(text, boxing=50):
    print("\n" * 1)
    print("-" * boxing)
    print(
        "|",
        " " * (boxing // 2 - len(text) // 2 - 3),
        color(214, text),
        " " * (boxing // 2 - len(text) // 2 - 3),
        "|",
    )
    print("-" * boxing)
    print("\n" * 2)


def query(text):
    return color(11, text)


def clear():
    os.system("cls")


def get_in(*set):
    y = input()
    while y not in set:
        print(
            CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE,
        )
        sys.stdout.flush()
        y = input()
    return y


def get_file(extension):
    y = input()
    while y and y.split()[-1] != extension:
        print("File needs to be of type : " + extension)
        print(
            CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE,
        )
        sys.stdout.flush()
        y = input()
    return y


class SetupStep:
    header = ""

    def __init__(self, header="") -> None:
        self.header = header


def setup_step(step: SetupStep = None, question: str = ""):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            clear()
            if SetupStep:
                heading(step.header)
            if question:
                print(query(question))
            return func(*args, **kwargs)

        return wrapper

    return decorator


INTERFACE = SetupStep("SETTING UP THE INTERFACE LAYER")
LOGGING = SetupStep("LOGGING SETUP")
NGAC = SetupStep("NGAC SETUP")
ABE = SetupStep("ABE SETUP")


@setup_step(LOGGING, "What should the debug level be? (INFO,DEBUG,ERROR)")
def LOGGING_LEVEL(cfg):
    print("This determines what data is logged to the log file")
    opt = get_in("INFO", "DEBUG", "ERROR")
    cfg.cfg["logging"]["level"] = opt


@setup_step(
    LOGGING, "Where should the log be stored? (relative to interface_layer folder)"
)
def LOGGING_LOCATION(cfg):
    cfg.cfg["logging"]["folder"] = input("Folder = ")


@setup_step(LOGGING, "What should the max file size be?")
def LOGGING_SIZE(cfg):
    print("default is 10000000 bytes press enter to keep this")
    inp = input()
    while not inp or not inp.isalnum():
        if not inp:
            break
        inp = input()
    if inp:
        cfg.cfg["logging"]["maxBytes"] = inp


@setup_step(INTERFACE)
def ACCEPT(target_name: str, fmt: str, callback: Callable, args):
    print(
        f"""The current {target_name} config is:
{fmt}

Is this ok? y/n ( choosing no here will restart the setup )
    """
    )
    y = get_in("y", "n")
    if y != "y":
        callback(args)


def SET_LOGGING(*args):
    global cfg
    LOGGING_LEVEL(cfg)
    LOGGING_LOCATION(cfg)
    LOGGING_SIZE(cfg)
    ACCEPT("Logging", cfg.logging(), args, SET_LOGGING)


@setup_step(NGAC, "What should the default policy be?")
def NGAC_POLICY(cfg):
    print("this needs to be a valid .pl file")
    inp = input("file = ")
    if inp:
        cfg.cfg["NGAC"]["policy"] = inp


@setup_step(NGAC, "Where is the NGAC admin_token stored?")
def NGAC_KEY(cfg):
    print("This path is relative to the interface_layer folder")
    inp = input("file = ")
    if inp:
        cfg.cfg["NGAC"]["admin_token"] = inp


@setup_step(NGAC, "What is the NGAC server ip?")
def NGAC_URL(cfg):
    def valid_url(text: str) -> bool:
        m = re.findall(r"\d+\.\d+\.\d+\.\d+\:\d+", text)
        if m:
            return m[0]
        else:
            return None

    inp = valid_url(input("url = "))
    while not inp:
        print(
            CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE,
        )
        sys.stdout.flush()
        inp = valid_url(input("url = "))
    cfg.cfg["NGAC"]["url"] = inp


def SET_NGAC(*args):
    global cfg
    NGAC_POLICY(cfg)
    NGAC_KEY(cfg)
    NGAC_URL(cfg)
    ACCEPT("NGAC", cfg.NGAC(), args, SET_NGAC)


@setup_step(ABE, "What is the URL to the ABE server?")
def ABE_URL(cfg):
    def valid_url(text: str) -> bool:
        m = re.findall(r"\d+\.\d+\.\d+\.\d+\:\d+", text)
        if m:
            return m[0]
        else:
            return None

    inp = valid_url(input("url = "))
    while not inp:
        print(
            CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE,
        )
        sys.stdout.flush()
        inp = valid_url(input("url = "))
    cfg.cfg["ABE"]["url"] = inp


def SET_ABE(*args):
    global cfg
    ABE_URL(cfg)
    ACCEPT("ABE", cfg.ABE(), args, SET_NGAC)


def optional(target_name: str, fmt: str, target_function: Callable, *args):
    clear()
    heading(INTERFACE.header)
    print(
        f"""Default {target_name} settings are:
-------------------
{fmt}
-------------------
    """
    )
    print(query(f"Do you want to change {target_name}? y/n"))
    y = get_in("y", "n")
    if y == "y":
        target_function(args)


def INTERFACE_SETUP(*args) -> Callable:
    global cfg
    optional("logging", cfg.logging(), SET_LOGGING)
    optional("NGAC", cfg.NGAC(), SET_NGAC)
    optional("ABE", cfg.ABE(), SET_ABE)


if __name__ == "__main__":
    """
    Sets up all of the configuration files for NGAC, InterfaceLayer and app

    Usage :
    ```bash
    python setup.py
    ```
    """
    INTERFACE_SETUP()
    clear()
    heading("Save file")
    with open("./src/interface_layer/data/SERVER.ini", "w") as f:
        f.writelines(cfg.render())
    clear()
    heading("That's it thank you for using the setup tool")
