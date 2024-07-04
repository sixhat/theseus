#!/usr/bin/env python
# encoding: utf-8


__author__ = 'David M.S. Rodrigues <dmsrs@iscte.pt>'

__doc__ = """
For a list of TXT files create a bag of words of the k most used ones.

Input: a TXT file directory

Output: two files! a histogram of words and a bag of words choosen by
        the scientists.

        Usage: python bagOfWords.py <TXT DIRECTORY> [NUM_OF_WORDS]

        It will output a hist.dat file and an words.dat file.
"""
__dependencies__ = """
        This packages depends on some external libraries.
        For Stemming we use the package <stemming> from
        http://pypi.python.org/pypi/stemming/

        Install with "easy_install steamming"
"""
import os
import sys
import datetime
import codecs
from . import theseus
import glob
from stemming.porter2 import stem
from operator import itemgetter


def log(st):
    s = " ".join(['--', str(datetime.datetime.utcnow()), '--', st])
    f = open(str(os.getpid()) + '-bagOfwords.log', 'a')
    f.write(s + "\n")
    f.close()
    print(s)


def outputBagWords(wds, hist=True):
    f = codecs.open(str(os.getpid()) + '-bagwords.txt', 'w', encoding='utf-8')
    n = 1
    for w, k in wds:
        f.write(w + "\t" + str(n) + "\n")
        n += 1
    f.close()
    if hist:
        totalWords = sum([i for w, i in wds])
        f = codecs.open(str(os.getpid()) + '-bagwords-hist.txt', 'w',
                        encoding='utf-8')
        for w, k in wds:
            f.write(w + "\t" + str(k) + "\t" + str(k / totalWords) + "\n")
        f.close()

# TODO Validate ARGUMENTS HERE
if len(sys.argv) != 3 and len(sys.argv) != 2:
    print(__doc__)
    sys.exit(1)

path = sys.argv[1]
# check to see if path ends with slash (/)
if path[-1] != '/':
    path += '/'

if len(sys.argv) == 3:
    nwords = int(sys.argv[2])

log("Start Processing")

words = {}

dirList = glob.glob("".join([path, '*.txt']))

docs = []

# READ FILES INTO DocNode Objects
for file in dirList:
    try:
        f = codecs.open(file, 'r', encoding='utf-8')
        txt = f.read()
        f.close()
        doc = theseus.DocNode(len(docs), file, txt, ttl=100)
        docs.append(doc)
    except Exception as e:
        log(f"{e} - Problem reading file: " + file + " -- " + str(sys.exc_info()[0]))

log("Total Files Read : " + str(len(docs)))

# Extract All Sentences from the Documents and from all Words
# stem them and add them to the words dictionary.
for doc in docs:
    doc.extractSentences()
    for stc in doc.sentences:
        stc.cleanText()
        for word in stc.cleanedWords:
            stemed = stem(word.lower())
            if len(stemed) > 2:
                if stemed in words:
                    words[stemed] += 1
                else:
                    words[stemed] = 1

log("Stemming and word Bag Histogram constructed")
words = sorted(list(words.items()), key=itemgetter(1), reverse=True)

outputBagWords(words)
