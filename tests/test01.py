__author__ = 'david'

import timeit
import os,sys
import datetime, codecs
from numpy import array, genfromtxt
from scipy.cluster.vq import kmeans2, whiten, vq, kmeans
from scipy import dot

feat=genfromtxt('8209-features.txt')
K=6
f2=feat[:50,:10000]

def go():
    centroids, variance=kmeans(f2,K,  iter=20)
    labels, distance=vq(f2,centroids)

t=timeit.Timer('go()', 'from __main__ import go')
print t.timeit(4)
