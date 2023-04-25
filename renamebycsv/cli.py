#!/usr/bin/env python3

import argparse
import csv
import os
import re
from typing import Iterable
import logging


def find_all_candidates(input_dir: str, regex: str, recursive: bool):
    results = []
    for subitem in os.listdir(input_dir):
        subitem_path = os.path.join(input_dir, subitem)
        match = re.match(regex, subitem)
        if os.path.isdir(subitem_path) and recursive:
            logging.debug(f'Checking directory "{subitem}"...')
            results.extend(find_all_candidates(subitem_path, regex, recursive))
        else:
            if not match:
                logging.debug(f'Ignoring "{subitem}"...')
                continue
            results.append((subitem_path, subitem, match))
            logging.debug(f'Collecting "{subitem}"...')
    return results


def rename(
    csv_path: str,
    candidates: Iterable[tuple[str, str, re.Match]],
    current: str,
    become: str,
    dry: bool,
    keep_extension: bool,
):
    replacement_dict = {}
    with open(csv_path, "r") as csv_fd:
        reader = csv.reader(csv_fd)
        current_col_ind = None
        become_col_ind = None
        for row in reader:
            if current_col_ind is None and become_col_ind is None:
                current_col_ind = row.index(current)
                become_col_ind = row.index(become)
                continue
            if (
                row[current_col_ind] in replacement_dict
                and replacement_dict[row[current_col_ind]] != row[become_col_ind]
            ):
                raise Exception("Duplicate current key.")
            replacement_dict[row[current_col_ind]] = row[become_col_ind]
    for subitem_path, subitem, match in candidates:
        if match.group(1) not in replacement_dict:
            logging.warning(
                'Group "%s" was not matched to any row in the provided CSV. '
                "Skipping...",
                match.group(1)
            )
            continue
        original = subitem_path
        objective = os.path.join(
            os.path.dirname(subitem_path),
            re.sub(match.re, replacement_dict[match.group(1)], subitem.strip()),
        )
        if keep_extension:
            objective += os.path.splitext(subitem_path)[1]
        logging.info(f'Will rename "{original}" to "{os.path.basename(objective)}"')
        if os.path.exists(objective):
            logging.error(
                f'Path at "{objective}" exists, not continuing. '
                "Use -f to overwrite instead of stopping."
            )
            exit(1)
        if not dry:
            os.rename(original, objective)
    if dry:
        logging.info("No file names were modified.")


def run(args):
    candidates = find_all_candidates(args.input_dir, args.regex, args.recursive)
    rename(
        args.csv, candidates, args.current, args.become, args.dry, args.keep_extension
    )


def main():
    program_name = "renamebycsv"
    argparser = argparse.ArgumentParser(
        program_name, "Rename all files by using a CSV as a dictionary."
    )
    argparser.add_argument(
        "input_dir",
        help="The directory containing the items that is to be renamed.",
        metavar="I",
    )
    argparser.add_argument(
        "regex",
        help="The regex to apply to each file name. The first capture group is used to "
        "perform the replacement.",
        metavar="R",
    )
    argparser.add_argument(
        "csv",
        help="The CSV to use as the dictionary for the substitutions in file name.",
        metavar="C",
    )
    argparser.add_argument(
        "current",
        help="The column header to look for the text matched by the regex.",
        metavar="F",
    )
    argparser.add_argument(
        "become", help="The column header to replace the regex match.", metavar="T"
    )
    argparser.add_argument(
        "-r",
        "--recursive",
        help="Perform renaming action recursively",
        action="store_true",
    )
    argparser.add_argument(
        "-f",
        "--force",
        help="Overwrite files if file already exists",
        action="store_true",
    )
    argparser.add_argument(
        "-d", "--dry", help="Do not perform any renames", action="store_true"
    )
    argparser.add_argument(
        "-V",
        "--verbosity",
        help="Set the logging verbosity",
        required=False,
        type=str,
        default="INFO",
    )
    argparser.add_argument(
        "-k",
        "--keep-extension",
        help="Keeps the original file's extension by appending it to the end of the "
        "name defined by the CSV.",
        action="store_true",
    )

    args = argparser.parse_args()
    logging.basicConfig(
        format="[%(filename)s %(asctime)s - %(levelname)s] %(message)s",
        level=args.verbosity.upper(),
    )
    run(args)


if __name__ == "__main__":
    main()
