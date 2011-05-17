#!/usr/bin/env python

import sys
import optparse

#from pygraph.classes.graph import graph
from pygraph.classes.digraph import digraph
#from pygraph.algorithms.searching import breadth_first_search
from pygraph.algorithms.minmax import heuristic_search, shortest_path
from pygraph.readwrite.dot import write

from common_graph import *

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

    # add fake end node
    end_node = GNode(-1, 'end', -1, 'end')
    gr.add_node(end_node)
    #real_end_nodes = [n for n in gr.nodes() if len(gr.neighbors(n))==0]
    real_end_nodes = [n for n in gr.nodes() if (n.i >= len(s1)) and (n.j >= len(s2))]
    for n in real_end_nodes:
        gr.add_edge((n, end_node), wt=0)

    # use A* without considering heuristic, which degenerates into a dijkstra
    opt = heuristic_search(gr, gr.get_node(0, 0), end_node, lambda s, e:0)
    print_align(opt)

    # get all shortest paths
    # this dijkstra implementation finds ALL paths, which is not needed
    #paths, costs = shortest_path(gr, gr.get_node(0, 0))
    ## get all possible end nodes
    #end_nodes = [n for n in gr.nodes() if len(gr.neighbors(n))==0]
    #best_end =  min(end_nodes, key=costs.get)
    #print 'Best alignment: %s' %paths[best_end]
    #print 'Cost: %d' %costs[best_end]

