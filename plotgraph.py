#!/usr/bin/env python

import sys
import optparse

#from pygraph.classes.graph import graph
#from pygraph.classes.digraph import digraph
#from pygraph.algorithms.searching import breadth_first_search
#from pygraph.algorithms.minmax import heuristic_search, shortest_path
from pygraph.readwrite.dot import write

import gv

from common_graph import build_graph

if __name__=='__main__':
    parser = optparse.OptionParser()
    options, args = parser.parse_args()
    if len(args) < 2:
        parser.print_help()
        sys.exit(1)

    s1, s2 = args
    if len(s1)<len(s2):
        s1, s2 = s2, s1

    gr = build_graph(s1, s2)

    # print the graph
    dot = write(gr)
    grv = gv.readstring(dot)
    gv.layout(grv, 'dot')
    gv.render(grv, 'svg', 'graph.svg')


