__author__ = 'david'

import os
import networkx as nx
import time
import datetime

inf = '5-guardianDoc.gml'
data = '/Volumes/HD2/PAPER-ACS/guardian.co.uk-2011-12-01/HTML/'
txt = '/Volumes/HD2/PAPER-ACS/guardian.co.uk-2011-12-01/TXT2/'
members_file = 'members.txt'


def log(st):
    s = " ".join(['--', str(datetime.datetime.utcnow()), '--', st])
    f = open(str(os.getpid()) + '-cluster.log', 'a')
    f.write(s + "\n")
    f.close()
    print(s)


def compareFiles(x, y):
    assert isinstance(x, str) or isinstance(x, str)
    assert isinstance(y, str) or isinstance(x, str)
    x = x.split('__')
    y = y.split('__')
    fmt = '%Y-%m-%d_%Hh%Mm%Ss'
    a = time.strptime(x[0], fmt)
    b = time.strptime(y[0], fmt)
    if a > b:
        return 1
    elif a < b:
        return -1
    else:
        return 0

g = nx.read_gml(inf, relabel=True)

print(nx.number_connected_components(g), "connected components")
print(g.number_of_nodes(), "nodes")


# Reading The Membership File
members = []
mf = open(members_file, 'r')
for linha in mf:
    if not linha.startswith("#"):
        members.append(linha.strip().split(' '))

for topic in members:
    topic.sort(cmp=compareFiles)
    print()
    print("<h1>NEW TOPIC</h1>")

    # Not good... need to travel the path.
    for doc in topic:
        print('<a href="%s">%s</a> - ' % (doc, doc))





