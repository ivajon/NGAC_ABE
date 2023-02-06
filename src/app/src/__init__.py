"""
Defines the arguments used for the app
"""
import argparse
import toml

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
    "-a", "--attributes",
    type=str,
    metavar="ATTRIBUTES",
)

# _________ COMMANDS _________

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

create_parser = sub.add_parser(
    "create",
    help="Create a new file on the server."
)

admin_parser = sub.add_parser(
    "admin",
    help="Admin commands."
)

admin_sub = admin_parser.add_subparsers(
    description="The following admin commands are available:",
    help="admin command",
    dest="admin_command"
)

##########################


def file(parser):
    parser.add_argument(
        "-f", "--file",
        type=str, default=None,
        metavar="FILE",
    )


# _________ READ _________

file(read_parser)

##########################

# _________ WRITE _________

file(write_parser)

write_parser.add_argument(
    "-i", "--input",
    type=str, default=None,
    metavar="INPUT",
    help="The input file to encrypt and upload."
)

###########################

# _________ DELETE _________

file(delete_parser)

###########################

# _________ Create ________

file(create_parser)

create_parser.add_argument(
    "-oa", "--object_attributes",
    metavar="object_attributes"
)

###########################


# Admin commands

admin_parser.add_argument(
    "-t", "--token",
    metavar="token",
    required=True
)

###########################

[
    readpol,
    loadi,
    assign,
    remove_assign,
] = [
    admin_sub.add_parser(
        x[0],
        help=x[1]
    ) for x in [
        ("readpol", "Reads the currently loaded policy from the NGAC server"),
        ("loadi", "Loads a policy from string"),
        ("assign", "Assign attribute to a user or object"),
        ("remove_assign", "Remove attribute assignment from user or object")
    ]
]

# _________ loadi _________

loadi.add_argument(
    "-i", "--input-file",
    metavar="file",
    required=True
)

###########################

# _________ assign ________

assign.add_argument(
    "-a", "--attribute",
    type=str,
    metavar="attribute", required=True
)

assign_grp = assign.add_mutually_exclusive_group(required=True)
assign_grp.add_argument(
    "-u", "--user",
    metavar="target_user"
)
assign_grp.add_argument(
    "-o", "--object",
    metavar="target_object"
)


###########################

# ________ unassign _______

remove_assign.add_argument(
    "-a", "--attribute",
    type=str,
    metavar="attribute", required=True
)

remove_assign_grp = remove_assign.add_mutually_exclusive_group(required=True)
remove_assign_grp.add_argument(
    "-u", "--user",
    metavar="target_user"
)
remove_assign_grp.add_argument(
    "-o", "--object",
    metavar="target_object"
)


###########################
