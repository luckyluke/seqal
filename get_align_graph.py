#!/usr/bin/env python

import sys
import optparse

#from pygraph.classes.graph import graph
from pygraph.classes.digraph import digraph
#from pygraph.algorithms.searching import breadth_first_search
from pygraph.algorithms.minmax import heuristic_search, shortest_path, shortest_path_bellman_ford
from pygraph.readwrite.dot import write

from common_graph import *
from heuristics import get_h, hlist

if __name__=='__main__':
    parser = optparse.OptionParser()
    parser.add_option('-H', '--heuristic',
            help='Choose the heuristic to be used with A*.',
            default='none', choices=hlist.keys())
    parser.add_option('-d', '--debug', help='Debug heuristic', action='store_true')
    options, args = parser.parse_args()
    if len(args) < 2:
        parser.print_help()
        sys.exit(1)

    s1, s2 = args
    if len(s1)<len(s2):
        s1, s2 = s2, s1

    gr = build_graph(s1, s2)

    ## add fake end node
    end_node = add_end_node(gr, s1, s2)

    ## use A* without considering heuristic, which degenerates into a dijkstra
    ##opt = heuristic_search(gr, gr.get_node(0, 0), end_node, lambda s, e:0)
    #print 'No heuristic (dijkstra)'
    #opt = heuristic_search(gr, gr.get_node(0, 0), end_node, get_h('none'))
    #print_align(opt)
    #print_cost(opt)

    #print '\nString_correlation'
    ##opt = heuristic_search(gr, gr.get_node(0, 0), end_node, get_h('sc', s1, s2, cmp=True, gr=gr))
    #opt = heuristic_search(gr, gr.get_node(0, 0), end_node, get_h('sc', s1, s2))
    #print_align(opt)
    #print_cost(opt)

    #print '\nMinimum residual cost'
    #opt = heuristic_search(gr, gr.get_node(0, 0), end_node, get_h('mrc', s1, s2, cmp=True, gr=gr))
    #print_align(opt)
    #print_cost(opt)

    hargs={}
    if options.debug:
        hargs = dict(cmp=True, gr=gr)

    print '\nHeuristic: %s' %options.heuristic
    #opt = heuristic_search(gr, gr.get_node(0, 0), end_node, get_h(options.heuristic, s1, s2, **hargs))
    #print opt
    #print_align(opt)
    #print_cost(opt)
    st, opt = shortest_path_bellman_ford(gr, gr.get_node(0, 0))
    n = end_node
    path = []
    while n:
        path.append(n)
        n = st[n]
    path.reverse()
    print_align(path)
    print 'Costo:',opt[end_node]

    # get all shortest paths
    # this dijkstra implementation finds ALL paths, which is not needed
    #paths, costs = shortest_path(gr, gr.get_node(0, 0))
    ## get all possible end nodes
    #end_nodes = [n for n in gr.nodes() if len(gr.neighbors(n))==0]
    #best_end =  min(end_nodes, key=costs.get)
    #print 'Best alignment: %s' %paths[best_end]
    #print 'Cost: %d' %costs[best_end]

