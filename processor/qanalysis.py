# encoding: utf-8
__author__ = 'david'
__version__ = '0.1.1'
__log__ = """
An Generic Q-analysis collection of scripts

* Shared Vertex Matrix
* Incidence Matrix
* save to JSON
* load to JSON

"""

import json
import argparse
import numpy
import networkx as nx
import os
import codecs


def usage():
    print("""
    USAGE:
        python qanalysis.py <file.tags> <separator>

    Example:
        python qanalysis guardian.tags :
    """)


def json_graph(graph, file='graph.json'):
    """
    Save graph to json object file
    """
    f = open(file, 'w')
    json.dump(graph, f)
    f.close()


def load_graph(file='graph.json'):
    """
    Load graph from json object file
    """
    f = open(file, 'r')
    graph = json.load(f)
    f.close()
    return graph


def load_edge_file(file, sep=':'):
    """
    Loads the edge file into sets A and B and a graph and a reverse graph
    """
    f = codecs.open(file, 'r', 'utf-8')
    A = []
    B = []
    graph = {}  # direct graph
    rgraph = {}   # reverse graph
    for line in f:
        st = line.strip().split(sep)
        el = st[0].strip()
        ot = st[1].strip()

        if el == "ACEP":
            print(st)
            print(ot)
            # direct graph
        if el not in graph:
            A.append(el)
            graph[el] = {}
            graph[el]['name'] = el
            graph[el]['connected_to'] = []
        if ot not in graph[el]['connected_to']:
            graph[el]['connected_to'].append(ot)

        #reverse graph
        if ot not in rgraph:
            rgraph[ot] = {}
            rgraph[ot]['name'] = ot
            rgraph[ot]['connected_to'] = []
        if el not in rgraph[ot]['connected_to']:
            rgraph[ot]['connected_to'].append(el)
        if ot not in B:
            B.append(ot)

    f.close()
    return {'A': A, 'B': B, 'graph': graph, 'rgraph': rgraph}


def calc_incidence_matrix(graph):
    """ Computes the incidence matrix from a graph object
    """
    incidence_matrix = numpy.zeros((len(graph['A']), len(graph['B'])), dtype=int)
    print("-- computing Incidence Matrix - shape", incidence_matrix.shape)
    for s in list(graph['graph'].items()):
        for k in s[1]['connected_to']:
            sl = graph['A'].index(s[1]['name'])
            sc = graph['B'].index(k)
            incidence_matrix[sl, sc] = 1

    #print I
    numpy.savetxt("incidence.txt", incidence_matrix, fmt='%1d')
    return incidence_matrix


def calc_shared_vertex_matrix(graph, incidence=None):
    """ From a graph object and the incidence matrix,
    computes the shared face matrix.
    """
    if incidence is None:
        incidence = calc_incidence_matrix(graph)

    SVM = numpy.zeros((len(graph['A']), len(graph['A'])), dtype=int)
    print("-- computing Shared Face Matrix - shape ", SVM.shape)
    for line in range(len(incidence)):
        #print "-- processing line nr. ", line
        for col in range(line, len(incidence)):
            SVM[line, col] = numpy.dot(incidence[line, :], incidence[col, :])
            SVM[col, line] = SVM[line, col]
            #print SVM
    numpy.savetxt('shared_face.txt', SVM, fmt='%1d')
    return SVM

## ---- Program starts running here parsing command line options...

parser = argparse.ArgumentParser(
    description='Theseus Q-analysis Processor '\
                '' + __version__,
    epilog="[*] - Q-analysis is alpha state. Be"\
           " careful with its use.")

parser.add_argument('-t', '--tagfile', help='Tag file to load',
                    type=str)
parser.add_argument('-s', '--sep', help='Tag file Separator (defaults to : )',
                    type=str,
                    default=':')
parser.add_argument('-j', '--jsonfile', help='JSON file to load',
                    type=str)
parser.add_argument('--version', action='version',
                    version='%(prog)s ' + __version__)

args = parser.parse_args()

## Let's have an empty graph
g = {}

## Command line options are parsed so now let's act on them:
if args.tagfile is None and args.jsonfile is None:
    g = load_graph()
if args.tagfile is not None:
    g = load_edge_file(args.tagfile, args.sep)
elif args.jsonfile is not None:
    g = json.load(args.jsonfile)

## Here we have the Graph (g) ready to do calculations on top of.
## simplicial complex
json_graph(g)


## incidence matrix
incidence_matrix = calc_incidence_matrix(g)

## Shared Vertex Matrix
SVM = calc_shared_vertex_matrix(g, incidence_matrix)

## Algoritmo para calcular os simlex de diferentes q-order e as q-chains




print("-- Incidence Matrix")
print(incidence_matrix)
print("-- Shared Vertex Matrix")
print(SVM)


#print "Maximum value of SVM ", SVM.max()
#print "Mean value of SVM ", SVM.mean()

def calculate_sets_q(sets, A):
    all = []
    for x in range(len(sets)):
        #print "-- %d" %x
        if len(sets[x]) > 0: #and sets[x] not in all:
            comp = sets[x]

            ## First check to see if this comp is a subset of a final (all)
            # set, this meaning that we don't need to compute it.
            b = False
            for a in all:
                if comp <= a: # equivalent to comp.issubset(a)
                    b = True
                    break
            if (b):
                continue

            # the component that we ara analysing now isn't part of a
            # component yet so we need to union it with others
            #print "-- initial" , comp
            for s in sets:
                if s.issubset(comp):
                    continue
                if not comp.isdisjoint(s):
                    #print "-- union with",s
                    comp.update(s)
                    #print comp
                    if len(comp) == len(A):
                    #   print "-- FULL HOUSE"
                        return [comp]
            if comp not in all:
                all.append(comp)
    return all


def areConnected(a1, b1, q=1):
    a = set(a1['connected_to'])
    b = set(b1['connected_to'])
    if (len(a.intersection(b)) >= q):
        return True
    else:
        return False

for q in range(SVM.max()):
    sets = []
    print("")
    print("-- %d-connected Matrix" % q)
    #print SVM*(SVM>=(q+1))
    for row in SVM:
        a = numpy.where(row >= (q + 1))
        sets.append(set(a[0]))
        #print sets
    #print set(SVM)

    print("-- q=", q)
    res = calculate_sets_q(sets, g['A'])
    print(res, "n.components:", len(res))

    for el in res:
        out = [g['A'][x] for x in list(el)]
        print("-- " + " ::: ".join(out))

    # Export network in a readable format
    out_file = str(q) + ('-%d' % os.getppid())
    G = nx.Graph()
    for el in res:
        out = [g['A'][x] for x in list(el)]

        G.add_nodes_from(out)

        for x in range(len(out)):
            for y in range(x + 1, len(out)):
                a = g['graph'][out[x]]
                b = g['graph'][out[y]]
                if areConnected(a, b, q):
                    G.add_edge(out[x], out[y])

    #nx.write_pajek(G, outf+'.net')
    #nx.write_weighted_edgelist(G, outf+'.edge', delimiter=',')
    #nx.write_gexf(G, outf+'.gexf')
    #nx.write_gml(G, outf+'.gml')
    nx.write_graphml(G, out_file + '.graphml', encoding='utf-8')






