__author__ = "david"
__doc__ = (
    r"Extract Titles from HTML Pages."
    r" Requires BeatutifullSoup"
    r"Argument is the directory where the "
)

import sys
import glob
import codecs
from BeautifulSoup import BeautifulSoup


def getTitle(doc):
    # Read HTML File
    tf = codecs.open(doc, "r", encoding="utf-8")
    html = tf.read()
    tf.close()
    soup = BeautifulSoup(html)
    return soup.html.head.title.string


# Need to process the Titles Of a a Folder.
infs = glob.glob(sys.argv[1] + "*.html")
outf = open("title.txt", "w")

for file in infs:
    try:
        str = file[2:] + "\t" + getTitle(file) + "\n"
    except:
        print("Problems with file:", file)
    print(str)
    outf.write(str.encode("utf-8"))
    outf.flush()
