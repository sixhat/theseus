# coding=utf-8
import os, sys
from operator import itemgetter
__author__ = 'david'
__doc__="""Extract Unique Labels"""

file = open(sys.argv[1],"r")

labels=[]
lhist={}

for l in file:
    s=l.split(":")
    label=s[1].strip()
    print s[0], label
    if label not in labels:
        labels.append(label)
    if lhist.has_key(label):
        lhist[label]+=1
    else:
        lhist[label]=1

file.close()

print labels, len(labels)
lhist = sorted(lhist.items(), key=itemgetter(1), reverse=True)
print lhist
