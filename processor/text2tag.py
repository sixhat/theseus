#!/usr/bin/env python
# encoding: utf-8
"""
text2tag.py
===========

Converts HTML files to TXT according to the Text to Tag ratio proposed by [Weninger2008]_

Usage:
``$ python text2tag.py <inputfile> <smooth-radius>``

.. rubric:: References
..  [Weninger2008] Weninger, T., & Hsu, W. H. (2008). Text Extraction from the Web via Text-to-Tag Ratio. 2008 19th International Conference on Database and Expert Systems Applications, 23-28. Ieee. doi: 10.1109/DEXA.2008.12.


"""

import sys
import re
import html.parser
import numpy
#from scipy import stats

# Global Parameters
infile = ''
sradius = 1

class MyStripper(html.parser.HTMLParser):
    """docstring for MyStripper"""

    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        """docstring for handle_data"""
        self.fed.append(d)

    def get_fed_data(self):
        return ''.join(self.fed)


def rm_head(string):
    """rm_head: Removes everything in the <head></head> of the document"""
    HEADTag = re.compile('(?s)<head.*?/head>')
    return HEADTag.sub('', string)


def rm_scripts(string):
    """rm_scripts: Removes <scripts> and Comments <!-- --> from html files"""
    SCRIPTtag = re.compile('(?s)<script.*?/script>')
    COMTag = re.compile('(?s)<!--.*?-->')
    #    FORMtag=re.compile('(?s)<form.*?/form>')
    INPUTtag = re.compile('(?s)<input.*?/>')
    return INPUTtag.sub('', SCRIPTtag.sub('', COMTag.sub('', string)))


def rm_tags(string):
    """rm_tags: Removes HTML Tags from string"""
    x = MyStripper()
    x.feed(string)
    return x.get_fed_data()


def rm_blank_lines(string):
    """removes blank lines from a string"""
    out = string.split("\n")
    for i in range(len(out) - 1, -1, -1):
        out[i] = out[i].strip(" \t")
        if len(out[
               i]) < 3: #Changed this to 3 to be consistent with the minimal char count for a word to be considered.
            out.pop(i)
            #pass
    return '\n'.join(out)


def process(infile):
    """Process the html infile"""
    # Load the file into a String
    f = open(infile, 'r')
    fil = f.read()
    f.close()

    fil = fil.decode("utf-8")

    # Remove the head section of the HTML
    fil = rm_head(fil)

    # Remove Scripts <script /script> and code comments <!-- -->
    fil = rm_scripts(fil)
    # Remove HTML Tags
    #fil=rm_tags(fil)
    #Remove Blank Lines
    fil = rm_blank_lines(fil)

    #Iterate over all lines in the document
    lines = fil.split("\n")
    score = []
    for line in lines:
        ntags = line.count("<")
        ltext = len(rm_tags(line))
        if ntags > 0:
            sc = (ltext + 0.0) / (ntags)
        else:
            sc = ltext + 0.0
        score.append(sc)

    smooth = score[:]

    if sradius > 0:
        for it in range(sradius, len(smooth) - sradius):
            smooth[it] = numpy.sum(score[(it - sradius):(it + sradius)]) / (
            2 * sradius + 1)

    mscore = numpy.mean(score)
    sscore = numpy.std(score)
    msmooth = numpy.mean(smooth)
    ssmooth = numpy.std(smooth)

    #    print "smooth radius:", sradius
    #    print "mean", "std","smoothed_mean", "smoothed_std"
    #    print mscore,sscore,msmooth,ssmooth, msmooth+ssmooth

    for it in range(len(lines)):
    #        if smooth[it]>(mscore+sscore):
        if smooth[it] > (msmooth + ssmooth):
            print(rm_tags(lines[it]).encode("utf-8"))
            #print score[it],smooth[it], rm_tags(lines[it]).encode("utf-8")

            #print fil


def main():
    global infile
    global sradius
    infile = sys.argv[1]
    sradius = int(sys.argv[2])

    #    print infile, sradius
    process(infile)


if __name__ == '__main__':
    if len(sys.argv) == 3:
        main()
    else:
        print(__doc__)
