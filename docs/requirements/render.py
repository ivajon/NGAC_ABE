"""
Regex replaces all [[table name]] with the table.

A table is a general markdown table with a header row and a separator row.
"""
import re
import sys

# Import arg parser
import argparse
import csv
from csv_tt import csv_to_md_table


def main():
    # Create the parser
    my_parser = argparse.ArgumentParser(
        description="Regex replaces all [[table name]] with the table."
    )

    # Add the arguments
    my_parser.add_argument(
        "MD", metavar="md", type=str, help="the template MD file to read"
    )
    my_parser.add_argument("OUT", metavar="out", type=str, help="the MD file to write")

    # Execute the parse_args() method
    args = my_parser.parse_args()

    # Read the MD file
    with open(args.MD, "r") as mdfile:
        md = mdfile.read()
    # Find all tables in the MD file
    tables = re.findall(r"\[\[table ([^\]]+)\]\]", md)
    # Read all the files and replace the tables
    for table in tables:
        if table.endswith(".csv"):
            with open(table, newline="") as csvfile:
                data = list(csv.reader(csvfile))
                md = md.replace(f"[[table {table}]]", "".join(csv_to_md_table(data)))
        else:
            with open(table, "r") as tablefile:
                md = md.replace(f"[[table {table}]]", tablefile.read())
    # Write the MD file
    with open(args.OUT, "w") as mdfile:
        mdfile.write(md)


if __name__ == "__main__":
    main()
