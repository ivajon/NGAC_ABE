from configparser import ConfigParser
pars = ConfigParser()
pars.read("data/SERVER.ini")
url = pars.get("NGAC", "url")
