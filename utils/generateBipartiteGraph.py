__author__ = 'david'
__log__ = """
Generate a simple Bipartite Tag Graph

0.1.0 - Simple working example with
"""
__version__="0.1.0"

import sys
import random
import argparse

def writeTags(graph, outfile='graph.tags'):
    fo = open(outfile, 'w')
    for el in graph:
        fo.write("%s %s\n" % el)
    fo.close()



parser = argparse.ArgumentParser(description='Simple Bipartite Graph ' \
                                             'generator')

parser.add_argument('a', type=int, help="Number of elements on set A",
                    default=10)
parser.add_argument('b', type=int, help="Number of elements on set B",
                    default=10)
parser.add_argument('d', type=int, help="Average outdegree of set A " \
                                         "elements")
parser.add_argument('-o', '--outfile', help='output file where to save the ' \
                                            'edge graph (default=graph.tags)' \
                                            '', default='graph.tags')
args=parser.parse_args()

na = args.a
nb = args.b
deg = 2*args.d


setA = range(na);
setB = range(na, (na + nb))


edges=[]
for a in setA:
    for _b in range(deg):
        if random.random()>0.5:
            b=random.choice(setB)
#            print a, b
            edges.append(("a"+str(a),"b"+str(b)))

writeTags(edges, args.outfile)

print "Graph saved to", args.outfile









