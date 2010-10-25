#!/usr/bin/env python
# encoding: utf-8
"""
cleanDuplicates.py
==================

Clean files with the same contents from a folder, keeping the oldest one.

usage: ``$ python cleanDuplicates.py DIR_TO_CLEAN``

"""

import sys
import os

def main():
    """ receives as argument the dir to clean
    """
    global indir
    
    files=[]
    ct=0
    cl=0
    for filename in os.listdir(indir):
        if filename[-4:]==".txt":
            ct+=1
            f=open(indir+filename,'r')
            txt=f.read()
            f.close()
            if files.count(txt)==0:
                files.append(txt)
            else:
                print "Unlinking", filename
                cl+=1
                os.unlink(indir+filename)
    
    if cl > 0:
        print "Cleaned", cl, "duplicates"

if __name__ == '__main__':
    if len(sys.argv)==2:
        indir=sys.argv[1]
        print "Setting In Dir to:", indir
        main()
    else:
        print __doc__