from configparser import ConfigParser
pars = ConfigParser()
pars.read("data/SERVER.ini")
url = pars.get("NGAC", "url")
current_policy = ""


def set_current_policy(pol):
    global current_policy
    current_policy = pol
