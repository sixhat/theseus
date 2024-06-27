# coding=utf-8
import os
import sys
import datetime
from numpy import   loadtxt, zeros, savetxt
from scipy.cluster.vq import   vq, kmeans
from scipy import dot
import math

__author__ = 'david'
__doc__ = """
Performs k-means clustering on a matrix of features

Input:
        * A file with the features matrix MxN where M is the number of
            observations and N is the number of features
        * The desired number of clusters K
        * The range of features to work with
            ex:
                4 # means 0...3
                4:10 # means elements 4...9
                4: # means 4...
                :7 # means 0....6

                Attention that this range starts index at 0 while the
                documents index start at 1 so 0 corresponds to 1

Output:
        A file with the indexes of the clusters

Usage:
        python cluster.py <features.txt> <K> <range>
"""

def log(st):
    s = " ".join(['--', str(datetime.datetime.utcnow()), '--', st])
    f = open(str(os.getpid()) + '-cluster.log', 'a')
    f.write(s + "\n")
    f.close()
    print(s)

# TODO Validate ARGUMENTS HERE
if len(sys.argv) < 3:
    print(__doc__)
    sys.exit(1)

Xfile = sys.argv[1]

K = int(sys.argv[2])

log("Loading features")

sK = 0
eK = 0
if len(sys.argv) == 4:
    rK = sys.argv[3].split(":")
    if len(rK) == 1:
        try:
            eK = int(rK[0])
        except ValueError:
            pass
    if len(rK) == 2:
        try:
            sK = int(rK[0])
        except ValueError:
            pass
        try:
            eK = int(rK[1])
        except ValueError:
            pass

ft = loadtxt(Xfile, skiprows=sK)

if eK < 3:
    eK = len(ft)
if eK > len(ft):
    eK = len(ft)
if sK < 0:
    sK = 0

if eK <= sK:
    log("Range is empty")
    sys.exit(1)

feat = ft[0:eK - sK, :]

log("Calculating Clusters for items %d through %d (inclusive)" % (sK + 1, eK))


# Normalize the features (Still have some doubts about the quality of
# results of this approach)
# feat=whiten(feat)

# The use of the Kmeans2 is giving crappy results as it is only running once.
# centroids, labels=kmeans2(feat,K, minit='points', iter=10)

# To use the Kmeans algorithm from scipy we get centroids and the variance and
# the iter parameter is not the iterations but the number of times to
# run kmeans
centroids, variance = kmeans(feat, K, iter=100)

log(
    "Centroids and Variance Calculated... proceeding to calculate Labels and Distance Matrix")
# But for this is necessary to compute the labels from the centroids (distance)
# from the features and the centroids.
labels, distance = vq(feat, centroids)

log("Labels length: " + str(len(labels)))

outputCluster = open("cluster-" + Xfile, "w")
for k in range(len(labels)):
    outputCluster.write(str(k + 1) + " " + str(labels[k] + 1) + "\n")
outputCluster.close()

log("Clusters Exported to file clusters-...")

log("Starting Display")
# A partir dos centroids pode-se calcular a distância de cada documento a cada
# um dos centroids com uma cor respectiva.
# Se desenharmos horizontalmente os pontos com X a ser a data de
# publicação e Y o cluster?
# O ideal será talvez utilizar o tkinter e o Canvas

from tkinter import *

root = Tk()
root.title("Clustering " + str(len(labels)) + " examples in " +
           str(K) + " clusters")
largura = 1400
altura = 700
ex = 2
bsize = 3

wstep = (0.0 + largura) / (len(labels) + 1.0)
hstep = altura / K
print(wstep)
print(hstep)

c = Canvas(root, width=largura, height=altura + hstep / ex)
c.pack()

def sim(a, b):
    return dot(a, b) / math.sqrt(dot(a, a) * dot(b, b))


# Calculate Similarity matrix to improve speed
distm = zeros((len(labels), len(labels)))
for i in range(0, len(labels)):
    for j in range(i, len(labels)):
        distm[i, j] = sim(feat[i, :], feat[j, :])
        distm[j, i] = distm[i, j]

log("Saving Similarity Matrix similarity-...")
savetxt("similarity-" + Xfile, distm)
# Start drawing...
lcen = []
pcen = []
text = []
arcs = []

def drawBack():
    for i in range(1, K + 1):
        lcen.append(c.create_line(0, hstep * i, largura, hstep * i))


def drawPoints():
    for i in range(0, len(labels)):
        x = (i + 1) * wstep
        y = (labels[i] + 1) * hstep
        pcen.append(c.create_rectangle(x - bsize, y - bsize,
                                       x + bsize, y + bsize, fill='red'))
        text.append(
            c.create_text(x, y + 40 - 10 * (i % 4), text=str(i + sK + 1),
                          activefill='blue', font=('arial', 9)))


def drawArcs(event):
    for el in arcs:
        c.delete(el)
    thresholdArcs = s.get()
    for i in range(0, len(labels)):
        x = (i + 1) * wstep
        y = (labels[i] + 1) * hstep
        for old in range(0, i):
        #            if dist(feat[old,:] ,feat[i,:] )<thresholdArcs:
            if distm[old, i] > thresholdArcs:
                oldx = (old + 1) * wstep
                oldy = (labels[old] + 1) * hstep
                if  abs(oldy - y) > 2:
                    arcs.append(c.create_line(oldx, oldy, x, y,
                                              fill='gray', activefill='blue'))
                else:
                    arcs.append(c.create_arc(oldx, y - hstep / ex, x,
                                             y + hstep / ex, start=0,
                                             extent=180, outline='gray',
                                             activeoutline='blue',
                                             activewidth=2.0))
    for el in arcs:
        c.tag_lower(el)

s = Scale(root, from_=0.0, to=1.0, resolution=0.01, orient=HORIZONTAL,
          label='Minimum Document Similarity:', length=0.6 * largura)
s.bind("<ButtonRelease-1>", drawArcs)
s.pack()
s.set(0.9)

drawBack()
drawPoints()
drawArcs(None)
#import cProfile
#cProfile.run('drawArcs(None)','drawArcs.prof')

mainloop()

log("Done")
