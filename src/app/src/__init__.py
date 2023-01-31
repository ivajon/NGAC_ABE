import argparse
import toml
import logging
from typing import List

project = toml.load("pyproject.toml")
__version__ = project["project"]["version"]
parser = argparse.ArgumentParser(
    prog="NGAC-ABE-CLI",
    usage="ngac-cli [options] [command] [command options]",
    description="A command line interface for attribute based access control and encryption.",
    epilog="This is a command line interface for attribute based access control and encryption. It is a part of the NGAC-ABE project.",
    add_help=True
)
parser.add_argument(
    "-v", "--version",
    action="version",
    version=f"%(prog)s {__version__}"
)
parser.add_argument(
    "-d", "--debug",
    action="store_true",
    help="Enable debug mode."
)


parser.add_argument(
    "-ip", "--url",
    type=str, default="localhost",
    metavar="SERVER_URL",
)

parser.add_argument(
    "-p", "--port",
    type=int, default=5000,
    metavar="SERVER_PORT",
)

parser.add_argument(
    "-nip", "--NGAC-IP",
    type=str, default=None,
    metavar="NGAC_SERVER_URL",
)

parser.add_argument(
    "-np", "--NGAC-port",
    type=int, default=None,
    metavar="NGAC_SERVER_PORT",
)
parser.add_argument(
    "-u", "--username",
    type=str,
)
parser.add_argument(
    "-k", "--key",
    type=str, default="admin_key",
    metavar="KEY",
)
parser.add_argument(
    "-a", "--attributes",
    type=str,
    metavar="ATTRIBUTES",
)

sub = parser.add_subparsers(
    description="The following commands are available:",
    help="command",
    dest="command"
)

read_parser = sub.add_parser(
    "read",
    help="Read a file from the server."
)

write_parser = sub.add_parser(
    "write",
    help="Write a file to the server."
)

delete_parser = sub.add_parser(
    "delete",
    help="Delete a file from the server."
)


# _________ READ _________

read_parser.add_argument(
    "-f", "--file",
    type=str, default=None,
    metavar="FILE",
)

##########################

# _________ WRITE _________

write_parser.add_argument(
    "-f", "--file",
    type=str, default=None,
    metavar="FILE",
)

write_parser.add_argument(
    "-i", "--input",
    type=str, default=None,
    metavar="INPUT",
    help="The input file to encrypt and upload."
)

###########################

# _________ DELETE _________

delete_parser.add_argument(
    "-f", "--file",
    type=str, default=None,
    metavar="FILE",
)

###########################
