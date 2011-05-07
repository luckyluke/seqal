#!/usr/bin/env python

import sys
import optparse

from pygraph.classes.graph import graph
from pygraph.classes.digraph import digraph
from pygraph.algorithms.searching import breadth_first_search
from pygraph.readwrite.dot import write

import gv

class GNode(object):
    def __init__(self, i, ch_i, j, ch_j):
        self.i, self.j = i, j
        self.ch_i, self.ch_j = ch_i, ch_j

    def __str__(self):
        return "(%d %d)" %(self.i, self.j)
    __repr__ = __str__

    def __hash__(self):
        # identify the node with the indexes of the chars in the 2 strings
        return hash((self.i, self.j))

    def __eq__(self, other):
        return hash(self) == hash(other)

def print_align(steps):
    s1, s2 = '', ''
    for i, step in enumerate(steps):
        if i < (len(steps)-1):
            next_step = steps[i+1]
            if (step.i < next_step.i) and (step.j < next_step.j):
                s1 += step.ch_i
                s2 += step.ch_j
            elif (step.i < next_step.i) and (step.j == next_step.j):
                s1 += step.ch_i
                s2 += '-'
            elif (step.i == next_step.i) and (step.j < next_step.j):
                s1 += '-'
                s2 += step.ch_j
            else:
                print 'error:',step, next_step
    print s1
    print s2

if __name__=='__main__':
    parser = optparse.OptionParser()
    options, args = parser.parse_args()
    if len(args) < 2:
        parser.print_help()
        sys.exit(1)

    s1, s2 = args
    if len(s1)<len(s2):
        s1, s2 = s2, s1

    # useful for test on the whole graph
    tot_len = len(s1)+len(s2)
    while len(s1) <= tot_len:
        s1 += '-'
    while len(s2) <= tot_len:
        s2 += '-'

    nodes = [[None]*len(s2) for k in range(len(s1))]
    nodes_all = []
    for i, chi in enumerate(s1):
        for j, chj in enumerate(s2):
            node = GNode(i, chi, j, chj)
            nodes[i][j] = node
            nodes_all.append(node)

    ## percorso tutto in alto
    #steps = [nodes[0][0], nodes[1][0], nodes[2][0], nodes[3][0], nodes[4][0], nodes[5][1], nodes[5][2]]
    ## percorso tutto in basso
    #steps = [nodes[0][0], nodes[0][1], nodes[0][2], nodes[1][3], nodes[2][3], nodes[3][4], nodes[4][4]]
    ## percorso inferiore sul parall
    #steps = [nodes[0][0], nodes[0][1], nodes[0][2], nodes[1][2], nodes[2][2], nodes[3][2], nodes[4][2]]
    ## percorso superiore sul parall
    #steps = [nodes[0][0], nodes[1][0], nodes[2][0], nodes[3][0], nodes[4][0], nodes[4][1], nodes[4][2]]

    #steps = [nodes[0][0], nodes[1][0], nodes[2][1], nodes[3][1], nodes[4][2]]
    #print_align(steps)

    gr = digraph()
    gr.add_nodes(nodes_all)
    for n in nodes_all:
        print n
        #if n.i <= len(s1.replace('-', '')) and n.j <= len(s2.replace('-', '')):
        do_keep_i, do_keep_j = False, False
        if n.i < (len(s1)-1) and n.j < len(s2):
            do_keep_i = True
            next_before = nodes[n.i+1][n.j]
            gr.add_edge((n, next_before))
            #print 'nb',next_before

        if n.i < len(s1) and n.j < (len(s2)-1):
            do_keep_j = True
            next_after = nodes[n.i][n.j+1]
            gr.add_edge((n, next_after))
            #print 'na',next_after

        if do_keep_i and do_keep_j:
            next_keep = nodes[n.i+1][n.j+1]
            gr.add_edge((n, next_keep))
            #print 'nk',next_keep

    dot = write(gr)
    grv = gv.readstring(dot)
    gv.layout(grv, 'dot')
    gv.render(grv, 'svg', 'graph.svg')

