# encoding: utf-8
import time
import datetime
import os
import sys
import glob

__author__ = 'David Rodrigues'
__doc__ = """
    This script renames the TXT files based on a sorting criteria.

    USAGE: python dateTimeSorter <path> <pattern>

    NOTE: if using wildcards *, ? include the pattern inside quotes

    EXAMPLE: python dateTimeSorter ./journal/ '*.txt'

        it expects that filenames are writen in the form: 2011-11-28_8h53m0s_15 de Março de 2012 20:53:23\_\_2728007653.html.txt
        It discards everything after the double underscores \_\_, but the first part has to comply to this format
""" 

def log(st):
    s = " ".join(['--', str(datetime.datetime.utcnow()), '--', st])
    f = open(str(os.getpid()) + '-cluster.log', 'a')
    f.write(s + "\n")
    f.close()
    print(s)


def compareFiles(x, y):
    assert isinstance(x, str)
    assert isinstance(y, str)
    x = x.replace(path, '').split('__')
    y = y.replace(path, '').split('__')
    fmt = '%Y-%m-%d_%Hh%Mm%Ss'
    a = time.strptime(x[0], fmt)
    b = time.strptime(y[0], fmt)
    if a > b:
        return 1
    elif a < b:
        return -1
    else:
        return 0


# Read Files
# TODO Validate ARGUMENTS HERE
if len(sys.argv) != 3:
    print(__doc__)
    sys.exit(1)

path = sys.argv[1]
patt = sys.argv[2]

if (path[-1] != '/'):
    path += '/'

# Sort Files by date
files = glob.glob("".join([path, patt]))
files.sort(cmp=compareFiles)

total = len(files)

for n in range(1, total + 1):
    str = 'f-%0.5d.txt' % n
    print(str, files[n - 1])
