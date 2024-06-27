__author__ = "david"
__doc__ = """
Swaps the columns of a tags file. Equivalent to transposing an incidence
matrix.
"""

import argparse

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("tagfile", help="The input tags file", type=open)
parser.add_argument("outfile", help="The output tags file", type=str)
parser.add_argument(
    "-s", "--sep", help="Field separator, defaults to <tab>", default="\t"
)

args = parser.parse_args()

fou = open(args.outfile, "w")
s = []

for line in args.tagfile:
    st = line.strip().split(args.sep)
    s.append(st[1] + args.sep + st[0] + "\n")
fou.writelines(s)
fou.close()
