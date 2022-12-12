"""
Reads a CSV file and writes to a MD file as a table.
"""

import csv
import sys

# Import arg parser
import argparse
from typing import List


def csv_to_md_table(data: List[List[str]]) -> List[str]:
    """
    From a csv file, return a list of strings, each string being a line in the
    markdown table.
    """
    table = []
    for index, row in enumerate(data):
        if index == 1:
            table.append("|")
            for item in row:
                table.append("---|")
            table.append("\n")
        table.append(f"| {' | '.join(row)} |")
        table.append("\n")
    return table


def main():
    # Create the parser
    my_parser = argparse.ArgumentParser(
        description="Reads a CSV file and writes to a MD file as a table."
    )

    # Add the arguments
    my_parser.add_argument("CSV", metavar="csv", type=str, help="the CSV file to read")
    my_parser.add_argument("MD", metavar="md", type=str, help="the MD file to write")

    # Execute the parse_args() method
    args = my_parser.parse_args()

    data = []
    # Read the CSV file
    with open(args.CSV, newline="") as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)

    # Write the MD file
    with open(args.MD, "w") as mdfile:
        mdfile.writelines(csv_to_md_table(data))


if __name__ == "__main__":
    main()
