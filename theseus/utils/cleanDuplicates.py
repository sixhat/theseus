"""
cleanDuplicates.py
==================

Clean files with the same contents from a folder.

usage: ``$ python cleanDuplicates.py DIR_TO_CLEAN``

"""

import os
import sys
import zlib
from typing import Set


def read_file_content(file_path: str) -> str:
    """Read and return the content of a file."""
    with open(file_path, "r") as f:
        return f.read()


def clean_duplicates(directory: str) -> tuple[int, int]:
    """
    Clean duplicate .txt files from the given directory.

    Returns a tuple of (total_files, cleaned_files).
    """
    unique_contents: Set[int] = set()
    total_files = 0
    cleaned_files = 0

    for filename in os.listdir(directory):
        if not filename.endswith(".txt"):
            continue

        total_files += 1
        file_path = os.path.join(directory, filename)
        content = read_file_content(file_path)

        key = zlib.crc32(content.encode())
        if key in unique_contents:
            print(f"Unlinking {filename}")
            os.unlink(file_path)
            cleaned_files += 1
        else:
            unique_contents.add(key)

    return total_files, cleaned_files


def main(directory: str) -> None:
    """Main function to clean duplicates in the given directory."""
    print(f"Setting In Dir to: {directory}")
    total_files, cleaned_files = clean_duplicates(directory)

    if cleaned_files > 0:
        print(f"Cleaned {cleaned_files} duplicates out of {total_files} total files")
    else:
        print(f"No duplicates found among {total_files} files")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print(__doc__)
