import csv
import logging
import os
import re
from typing import Iterable


def find_all_candidates(input_dir: str, regex: str, recursive: bool):
    logging.info(
        'Searching "%s" for files that match "%s" %s',
        input_dir,
        regex,
        "recursively" if recursive else "non-recursively",
    )
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
    if len(results) < 1:
        logging.info(
            'No results found matching "%s" in "%s". Please double check your REGEX '
            "pattern and directory being searched.",
            regex,
            input_dir,
        )
    else:
        logging.info("Collected %d files to rename.", len(results))
    return results


def rename_by_csv(
    csv_path: str,
    candidates: Iterable[tuple[str, str, re.Match]],
    current: str,
    become: str,
    dry: bool,
    extension: str,
    keep_extension: bool,
):
    replacement_dict = {}
    with open(csv_path, "r") as csv_fd:
        reader = csv.reader(csv_fd)
        current_col_ind = None
        become_col_ind = None
        for row in reader:
            if current_col_ind is None and become_col_ind is None:
                if current not in row:
                    logging.error("\"%s\" not in header %s.", current, list(row))
                if become not in row:
                    logging.error("\"%s\" not in header %s.", become, list(row))
                current_col_ind = row.index(current)
                become_col_ind = row.index(become)
                continue
            if (
                row[current_col_ind] in replacement_dict
                and replacement_dict[row[current_col_ind]] != row[become_col_ind]
            ):
                # Check if there's a duplicate key for different values.
                raise Exception("Duplicate current key.")
            replacement_dict[row[current_col_ind]] = row[become_col_ind]
    for subitem_path, subitem, match in candidates:
        if match.group(1) not in replacement_dict:
            logging.warning(
                'Group "%s" was not matched to any row in the provided CSV. '
                "Skipping...",
                match.group(1),
            )
            continue
        original = subitem_path
        objective = os.path.join(
            os.path.dirname(subitem_path),
            re.sub(match.re, replacement_dict[match.group(1)], subitem.strip()),
        )
        if extension:
            objective += ("." if not extension.startswith(".") else "") + extension
        if keep_extension:
            objective += os.path.splitext(subitem_path)[1]
        logging.info(f'Will rename "{original}" to "{os.path.basename(objective)}"')
        if os.path.exists(objective):
            logging.error(
                f'Path at "{objective}" already exists, not continuing. '
                "Use -f to overwrite instead of stopping."
            )
            exit(1)
        if not dry:
            os.rename(original, objective)
    if dry:
        logging.info("No file names were modified.")
