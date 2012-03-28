__author__ = 'david'
"""
Converts an Incidence matrix to a tags file
"""

import   argparse


parser = argparse.ArgumentParser(description='Convert an Incidence matrix to'\
                                             'a tags file')

parser.add_argument('incidence', type=file,
                    help='The Incidence Matrix File, '\
                         'can have header and rows. This will try to detect '\
                         ''\
                         'them')

parser.add_argument('outfile', type=str, help='The name of the '\
                                              'tags file you want to'\
                                              ' create')

parser.add_argument('-s', '--sep', type=str, default='\t',
                    help='Field Separator, defaults to <tab>')

args = parser.parse_args()

labels = True
lab = []

fou = open(args.outfile, 'w')

line = 0
for li in args.incidence:
    sp = li.strip().split(args.sep)
    if line == 0:
        if sp[0].isdigit():
            print "-- This looks like an unlabeled matrix"
            labels = False
        else:
            print "-- This looks like a labeled matrix"
            labels = True
            lab = sp[1:]
            line += 1
            continue
    if labels:
        els = [int(x) for x in sp[1:]]
        for el in range(len(els)):
            if els[el] > 0:
                st = sp[0] + args.sep + lab[el]
                print st
                fou.write(st + '\n')
    else:
        els = range(len(sp))
        for el in els:
            if int(sp[el]) > 0:
                st = str(line) + args.sep + str(el)
                print st
                fou.write(st + '\n')
    line += 1

fou.close()