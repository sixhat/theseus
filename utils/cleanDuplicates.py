#!/usr/bin/env python
# encoding: utf-8
"""
cleanDuplicates.py

Clean files with the same contents from a folder, keeping the oldest one.

usage:
        $ python cleanDuplicates.py DIR_TO_CLEAN

Created by David Rodrigues on 2010-02-22.
Copyright (c) 2010 Sixhat Pirate Parts. All rights reserved.
"""

import sys
import os

class DocNode:
    """docstring for DocNode"""
    idn=0
    txt=''
    fnm=''
    ttl=0
    def __init__(self, idn, fnm, txt, ttl):
        self.idn=idn
        self.fnm=fnm
        self.txt=txt
        self.ttl=ttl

def main():
    """docstring for main"""
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