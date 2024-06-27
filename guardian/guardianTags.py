# encoding: utf-8
__author__ = 'david'
__doc__ = """Genereates a network from the GuardinaTags """

import sys
import networkx
import codecs

inf = sys.argv[1]
k = int(sys.argv[2])

f = codecs.open(inf, 'r', encoding='utf-8')

docs = {}

ct = 0
for line in f:
    c = line.split(":")
    a = c[0].strip()
    b = c[1].strip()
    if a not in docs:
        docs[a] = [b]
    else:
        docs[a].append(b)
    ct += 1

# Create an empty  Graph
G = networkx.Graph()
for doc in list(docs.items()):
    #G.add_nodes_from(doc[1])

    for noi in doc[1]:
        for noj in doc[1]:
            if noi != noj:
                try:
                    G.edge[noi][noj]['weight'] += 1
                except KeyError:
                    G.add_edge(noi, noj, weight=1)

for e in G.edges():
    G.edge[e[0]][e[1]]['weight'] /= 2

print(len(G.nodes()))
print(len(G.edges()))

networkx.write_pajek(G, 'guardianTags.net')
networkx.write_weighted_edgelist(G, 'guardianTags.edge', delimiter=',')
networkx.write_gexf(G, 'guardianTags.gexf')
networkx.write_gml(G, 'guardianTags.gml')
networkx.write_graphml(G,'guardianTags.graphml')
#networkx.draw(G, networkx.spring_layout(G))
#plt.savefig("guardian.png",dpi=300 )
#plt.draw()


for ed in G.edges():
    print(G.nodes().index(ed[0]), G.nodes().index(ed[1]))




