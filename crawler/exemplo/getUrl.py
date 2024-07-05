#!/usr/bin/env python
# encoding: utf-8
"""
getUrl.py
=========

Parses a downloaded RSS file and downloads all items in the Feed

Usage:
    getUrl.py

"""

import sys
import os
import feedparser
import time
import zlib
import requests


def main():
    """
    This module receives as argument the folder where the rss.xml file is stored
    """
    # Parse the downloaded rss.xml file
    rss = feedparser.parse(str(sys.argv[1]) + "/rss.xml")
    urls = []  # The already downloaded list of URLS
    # Let's see if the downloaded list is present and construct the urls list
    try:
        urls_file = open(sys.argv[1] + '/urls.txt', 'r+')
        for line in urls_file:
            urls.append(line.split()[0])
    except Exception:
        urls_file = open(sys.argv[1] + '/urls.txt', 'w')

    # Let's iterate over all entries in the parsed RSS
    for item in rss.entries:
        if len(item.link) > 7:
            try:
                nome = str(item.updated_parsed[0]) + "-" + str(item.updated_parsed[1]) + "-" + str(
                    item.updated_parsed[2]) + "_"
                nome = nome + str(item.updated_parsed[3]) + "h" + str(item.updated_parsed[4]) + "m" + str(
                    item.updated_parsed[6]) + "s_"
            except Exception as e:
                print(f"Exception {e}")
                nome = time.strftime("%Y-%j_%H-%M-%S", time.gmtime())

            cifra = str(zlib.adler32(item.link.encode()))
            nome = nome + "_" + cifra + ".html"  # let's set the name of the output file based on the time

            if str(item.link).encode("utf-8") not in urls:

                r = requests.get(item.link)
                if r.status_code == 200:
                    out = open(sys.argv[1] + "/" + nome, 'w')
                    out.write(r.text)
                    out.close()
                else:
                    out2 = open(sys.argv[1] + "/" + "notfound.txt", 'a')
                    out2.write(str(item.link).encode("utf-8") + "\n")
                    out2.close()

                urls_file.write(item.link + "\n")  # Add this item to the downloaded URLS file
                urls_file.flush()  # Let's flush the internal buffer
                os.fsync(urls_file.fileno())  # Let's force write of all internal buffers to disk
                time.sleep(int(sys.argv[2]))  # Wait TIMEOUT seconds to avoid DDoS blacklistings...
    urls_file.close()


if __name__ == '__main__':
    if len(sys.argv) == 3:
        main()
    else:
        print(__doc__)
