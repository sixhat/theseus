'''
Extract Titles from HTML Pages.

    Usage: 
        python extractTitles.py directory

        directory must contain html files

    Outputs a file title.txt with all titles separated by a tab.
    Requires BeatutifullSoup to be installed in python environment
'''
__author__ = 'David Sousa-Rodrigues'

import sys
import os
import glob
from bs4 import BeautifulSoup

def getTitle(doc):
    '''Read HTML File and returns title'''
    with open(doc, 'r', encoding='utf-8') as tf:
        html = tf.read()
    soup = BeautifulSoup(html, 'html.parser')
    return soup.html.head.title.string

def main(dir):
    '''Extract the Titles Of a HTML files in dir.'''
    lines = [file + '\t' + getTitle(file) + '\n' for file in glob.glob(dir + '*.html')]
    with open('title.txt', 'w') as outf:
        outf.writelines(lines)

if __name__=='__main__':
    if len(sys.argv)==2 and os.path.isdir(sys.argv[1]):
        dir = sys.argv[1]
        if dir[-1]!='/':
            dir += '/'
        main(dir)
    else:
        print(__doc__)
