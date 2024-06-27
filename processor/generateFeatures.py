# encoding: utf-8
import glob
import time
import os
import sys
import datetime
import codecs
from . import theseus
import multiprocessing
from stemming.porter2 import stem

__author__ = 'david'
__doc__ = """
Generate The Examples Matrix of Features

Input:
                A Folder with TXT files to generate the Matrix of Features X
                A bagOfWords file

Output:
                A features.txt matrix with the features of X

Usage:
                python generateFeatures.py <DIR> <BagOfWords>

Notes:
                This script requires the multiprocessing package to take advantage
                of all the cores existing in the computer. Therefore is advisable
                to have free memory on the machine and at least python 2.6.

  """

# Some Classes
class ReturnValue:
    def __init__(self, words, docu):
        self.words = words
        self.docu = docu

# Some Functions --------------------------------------------------------------

def index(st, i):
    f = open(str(os.getpid()) + '-index.txt', 'a')
    f.write(str(i) + "\t" + st + "\n")
    f.close()


def log(st):
    s = " ".join(['--', str(datetime.datetime.utcnow()), '--', st])
    f = open(str(os.getpid()) + '-generateFeatures.log', 'a')
    f.write(s + "\n")
    f.close()
    print(s)


def outputFeatures(wds, b):
    f = codecs.open(str(os.getpid()) + '-features.txt', 'a', encoding='utf-8')
    #f=open('features.txt','a')
    n = 1
    feature = [0 for x in b]
    for w in wds:
        if w in b:
            feature[b[w] - 1] = 1
    try:
        f.write(" ".join([str(x) for x in feature]) + "\n")
    except:
        log("Feature Not Writen")
    f.flush()
    f.close()


def outputTFIDF(feat, bag):
    f = codecs.open(str(os.getpid()) + '-features-tfidf.txt', 'w',
                    encoding='utf-8')
    for doc in feat:
        feature = [0.0 for x in bag]
        for word, weight in list(doc.items()):
            if word in bag:
                feature[bag[word] - 1] = weight
        f.write(" ".join([str(x) for x in feature]) + "\n")
        f.flush()
    f.close()


def compareFiles(x, y):
    assert isinstance(x, str)
    assert isinstance(y, str)
    x = x.replace(path, '').split('__')
    y = y.replace(path, '').split('__')
    fmt = '%Y-%m-%d_%Hh%Mm%Ss'
    a = time.strptime(x[0], fmt)
    b = time.strptime(y[0], fmt)
    if a > b:
        return 1
    elif a < b:
        return -1
    else:
        return 0


def extractWords(doc):
    words = {}
    docu = []
    doc.extractSentences()
    for stc in doc.sentences:
        stc.cleanText()
        for word in stc.cleanedWords:
            stemed = stem(word.lower())
            docu.append(stemed)
            words[stemed] = 1
    return ReturnValue(words, docu)


def calcTFIDF(doc):
    words = {}
    for word in doc:
        if word not in words:
            words[word] = theseus.tfidf(word, doc, corpus)
    return words

# -----------------------------------------------------------------------------
# TODO Validate ARGUMENTS HERE
if len(sys.argv) != 3:
    print(__doc__)
    sys.exit(1)

path = sys.argv[1]
bagf = sys.argv[2]

log("Start Processing")

dirList = glob.glob("".join([path, '*.txt']))
dirList.sort(cmp=compareFiles)

docs = []

# Load bag of words
b = codecs.open(bagf, 'r', encoding='utf-8')
c = b.readlines()
b.close()

bag = {}
for l in c:
    s = l.split()
    bag[s[0]] = int(s[1])

log("Using Features Dimension: " + str(len(bag)))

# READ FILES INTO DocNode Objects
for file in dirList:
    try:
        f = codecs.open(file, 'r', encoding='utf-8')
        txt = f.read()
        f.close()
        doc = theseus.DocNode(len(docs), file, txt, ttl=100)
        docs.append(doc)
    except:
        log("Problem reading file: " + file + " -- " + str(sys.exc_info()[0]))

log("Total Files Read : " + str(len(docs)))

#Extract All Sentences from the Documents and from all Words stem them and add them to the words dictionary.
corpus = []

n = 1
for doc in docs:
    index(doc.fnm, n)
    n += 1

# Define a Pool of worker processes equal to the number of Cores we have.
log("Starting a Pool of " + str(multiprocessing.cpu_count()) + " Workers")
pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())

log("Applying the extractWords via pool.map")
allWords = pool.map(extractWords, docs)

for a in allWords:
    outputFeatures(a.words, bag)
    corpus.append(a.docu)

pool.close()
log("Corpus Created! Calculating TF.IDF Features Vector")

features = []

log("Starting a Pool of " + str(multiprocessing.cpu_count()) + " Workers")
pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())

log("Applying the calcTFIDF via pool.map")
features = pool.map(calcTFIDF, corpus)

log("Features Generation Completed! Exporting Features to File")
outputTFIDF(features, bag)

pool.close()
pool.join()

log("Construction of the Features Matrix Concluded")
log("Features Matrix is a " + str(len(docs)) + "x" + str(len(bag)) + " matrix")
