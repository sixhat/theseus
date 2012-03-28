__author__ = 'david'

import networkx as nx
import random
import argparse

def net_arenas(N=256, z1=13, z2=4, zout=1):
    nodes=range(N)
    edges=[]
    cs = N/4
    ss = cs/4

    for el in nodes:
        # z1
        for z in range(z1):
            ot = random.choice(nodes)
            while el==ot or el/ss != ot/ss:
                ot = random.choice(nodes)
            edges.append((el,ot))
        # z2
        for z in range(z2):
            ot = random.choice(nodes)
            while el==ot or el/cs != ot/cs or el/ss == ot/ss:
                ot = random.choice(nodes)
            edges.append((el,ot))
        #zout
        for z in range(zout):
            ot = random.choice(nodes)
            while el==ot or el/cs == ot/cs:
                ot = random.choice(nodes)
            edges.append((el,ot))


    print edges


    return edges


parser = argparse.ArgumentParser(description='Create an Arenas Network')

parser.add_argument('N', type=int)
parser.add_argument('z1', type=int)
parser.add_argument('z2', type=int)
parser.add_argument('zout', type=int)

a = parser.parse_args()

edges = net_arenas(a.N, a.z1, a.z2, a.zout)

G=nx.Graph()
G.add_edges_from(edges)

nx.write_graphml(G,'testGRaph.graphml')

