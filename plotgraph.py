#!/usr/bin/env python

import sys
import optparse

#from pygraph.classes.graph import graph
from pygraph.classes.digraph import digraph
#from pygraph.algorithms.searching import breadth_first_search
from pygraph.readwrite.dot import write

import gv

S = {'a':{'a':0, 'c':1, 'g':2, 't':1, '-':1},
     'c':{'a':1, 'c':0, 'g':3, 't':2, '-':2},
     'g':{'a':2, 'c':3, 'g':0, 't':1, '-':3},
     't':{'a':1, 'c':2, 'g':1, 't':0, '-':1},
     '-':{'a':1, 'c':2, 'g':3, 't':1, '-':99}
     }

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

class Graph(digraph):
    def get_node(self, i, j):
        for n in self.nodes():
            if (n.i == i) and (n.j == j):
                return n
        raise KeyError('Node (%d %d) not found!' %(i, j))

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

def weight_step(par, chl):
    # verify that par is the parent and chl the child
    if par.i > chl.i or par.j > chl.j:
        par, chl = chl, par
    if par.i == chl.i:
        h = '-'
    else:
        h = par.ch_i
    if par.j == chl.j:
        k = '-'
    else:
        k = par.ch_j
    return S[h][k]

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
    s1_pad, s2_pad = s1[:], s2[:]
    while len(s1_pad) <= tot_len:
        s1_pad += '-'
    while len(s2_pad) <= tot_len:
        s2_pad += '-'

    # build all nodes
    gr = Graph()
    for i, chi in enumerate(s1_pad):
        for j, chj in enumerate(s2_pad):
            # if we're out of both strings length we are comparing two gaps
            if (i <= len(s1) or j <= len(s2)):
                # can't have more than len(s1) gaps in s2 and vice versa
                if ((i >= j) and ((i-j) <= len(s1))) or ((i <= j) and ((j - i) <= len(s2))):
                    node = GNode(i, chi, j, chj)
                    gr.add_node(node)

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

    # add the links between the nodes
    for n in gr.nodes():
        for h, k in [(n.i+1, n.j), (n.i+1, n.j+1), (n.i, n.j+1)]:
            try:
                nn = gr.get_node(h, k)
            except KeyError, e:
                pass
            else:
                # if we're comparing a gap, there is only one way to go
                if (n.i >= len(s1) and (nn.i==n.i+1 and nn.j==n.j+1))\
                        or (n.j >= len(s2) and (nn.i==n.i+1 and nn.j==n.j+1)):
                    add_edge = True
                elif (n.i < len(s1) and n.j < len(s2)):
                    # if we compare two chars every direction is possible
                    add_edge = True
                else:
                    add_edge = False

                if add_edge:
                    wt = weight_step(n, nn)
                    gr.add_edge((n, nn), wt=wt)
                    print 'Added link from %s to %s, wt %d' %(n, nn, wt)

    #gr.parents = gr.incidents
    #gr.childs = gr.neighbors

    dot = write(gr)
    grv = gv.readstring(dot)
    gv.layout(grv, 'dot')
    gv.render(grv, 'svg', 'graph.svg')

