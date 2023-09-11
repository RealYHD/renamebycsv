#!/usr/bin/env python3

import argparse
import logging

from renamebycsv.renamer import find_all_candidates, rename_by_csv


def run(args):
    candidates = find_all_candidates(args.input_dir, args.pattern, args.recursive)
    if len(candidates):
        rename_by_csv(
            args.csv,
            candidates,
            args.current,
            args.become,
            args.dry,
            args.extension,
            args.keep_extension,
        )


def main():
    program_name = "renamebycsv"
    argparser = argparse.ArgumentParser(
        program_name, description="Rename all files by using a CSV as a dictionary."
    )
    argparser.add_argument(
        "input_dir",
        help="The directory containing the items that is to be renamed.",
        metavar="I",
    )
    argparser.add_argument(
        "pattern",
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
        help="Perform renaming action recursively.",
        action="store_true",
    )
    argparser.add_argument(
        "-f",
        "--force",
        help="Overwrite files if file already exists.",
        action="store_true",
    )
    argparser.add_argument(
        "-d", "--dry", help="Do not perform any renames", action="store_true"
    )
    argparser.add_argument(
        "-V",
        "--verbosity",
        help="Set the logging verbosity.",
        required=False,
        type=str,
        default="INFO",
    )
    argparser.add_argument(
        "-e",
        "--extension",
        help='Sets the new file extension after the renaming. Use empty string ("") '
        "to not add extension. Will use empty string by default.",
        type=str,
        default="",
        required=False,
    )
    argparser.add_argument(
        "-k",
        "--keep-extension",
        help="Keeps the OS recognized extension from the original filename. Will "
        'append to end of argument given by "-e" or "--extension".',
        action="store_true",
        default=False,
        required=False,
    )

    args = argparser.parse_args()
    logging.basicConfig(
        format="[%(filename)s %(asctime)s - %(levelname)s] %(message)s",
        level=args.verbosity.upper(),
    )
    run(args)


if __name__ == "__main__":
    main()
