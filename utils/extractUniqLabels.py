# coding=utf-8
import sys
from operator import itemgetter
__author__ = 'david'
__doc__="""Extract Unique Labels"""

file = open(sys.argv[1],"r")

labels=[]
lhist={}

for line in file:
    s=line.split(":")
    label=s[1].strip()
    print(s[0], label)
    if label not in labels:
        labels.append(label)
    if label in lhist:
        lhist[label]+=1
    else:
        lhist[label]=1

file.close()

print(labels, len(labels))
lhist = sorted(list(lhist.items()), key=itemgetter(1), reverse=True)
print(lhist)
