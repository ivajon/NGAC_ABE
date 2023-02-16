from configparser import ConfigParser

pars = ConfigParser()
pars.read("data/SERVER.ini")
url = pars.get("NGAC", "url")

# This is bad practice.
current_policy = ""


def set_current_policy(pol):
    global current_policy
    current_policy = pol


def get_policy(): return current_policy
