def start_ngac():
    from pep import PEP
    from ngac_server import NGACServer
    from cme import CME

    """
    Start the NGAC server
    """
    cme = CME()
    cme.start()
    pep = PEP()
    pep.start()
    ngac_server = NGACServer()
    ngac_server.start()
    return ngac_server, cme, pep


def stop_ngac(ngac_server, cme, pep):
    from pep import PEP
    from ngac_server import NGACServer
    from cme import CME

    """
    Stop the NGAC server
    """
    ngac_server.stop()
    cme.stop()
    pep.stop()


ngac_server, cme, pep = start_ngac()


def panic_handler(*args):
    stop_ngac(ngac_server, cme, pep)
    exit()


import atexit

atexit.register(panic_handler)
import sys

# Also shutdown the NGAC server if the script runs into an error
sys.excepthook = panic_handler
# What do to on sigint

while True:
    pass
