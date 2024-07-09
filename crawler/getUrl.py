#!/usr/bin/env python
# encoding: utf-8
"""
getUrl.py
=========

Parses a downloaded RSS file and downloads all items in the Feed

Usage:
    getUrl.py <folder> <timeout> <rss_url>

    folder is the folder where the rss.xml file was placed.
    timeout is in seconds
"""

import sys
import os
import feedparser
import time
import zlib
import requests
from typing import List


def load_urls(folder_path: str) -> List[str]:
    try:
        with open(f"{folder_path}/urls.txt", "r") as file:
            return [line.split()[0] for line in file]
    except FileNotFoundError:
        return []


def write_url(
    item: str,
    folder_path: str,
) -> None:
    with open(f"{folder_path}/urls.txt", "a") as file:
        file.write(item)


def generate_filename(item) -> str:
    try:
        updated = item.updated_parsed
        timestamp = f"{updated[0]:04d}-{updated[1]:02d}-{updated[2]:02d}_{updated[3]:02d}h{updated[4]:02d}m{updated[6]:02d}s"
    except Exception as e:
        print(f"Exception when parsing timestamp: {e}")
        timestamp = time.strftime("%Y-%j_%H-%M-%S", time.gmtime())

    cifra = str(zlib.adler32(item.link.encode()))
    return f"{timestamp}_{cifra}.html"


def download_item(item, folder_path: str) -> None:
    r = requests.get(item.link)
    if r.status_code == 200:
        filename = generate_filename(item)
        with open(os.path.join(folder_path, filename), "w", encoding="utf-8") as out:
            out.write(r.text)
    else:
        with open(os.path.join(folder_path, "notfound.txt"), "a") as out:
            out.write(f"{item.link}\n")


def download_rss(rss_url, folder_path: str) -> None:
    r = requests.get(rss_url)
    if r.status_code == 200:
        with open(os.path.join(folder_path, "rss.xml"), "w") as out:
            out.write(r.text)
    else:
        print("*** Error, no RSS to download")


def main(folder_path, timeout, rss_url):
    """
    This module receives as argument the folder where the rss.xml file is stored
    """
    download_rss(rss_url, folder_path)
    rss = feedparser.parse(str(sys.argv[1]) + "/rss.xml")
    urls = load_urls(folder_path)

    # Let's iterate over all entries in the parsed RSS
    for item in rss.entries:
        if len(item.link) > 7 and item.link not in urls:
            print(f"--- Processing {item.link}")
            download_item(item, folder_path)
            write_url(item.link + "\n", folder_path)
            urls.append(item.link)
            time.sleep(timeout)  # Wait TIMEOUT seconds to avoid DDoS blacklistings...


if __name__ == "__main__":
    if len(sys.argv) == 4:
        main(sys.argv[1], int(sys.argv[2]), sys.argv[3])
    else:
        print(__doc__)
