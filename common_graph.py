#!/usr/bin/env python

import sys
import optparse

#from pygraph.classes.graph import graph
from pygraph.classes.digraph import digraph
#from pygraph.algorithms.searching import breadth_first_search
#from pygraph.algorithms.minmax import heuristic_search, shortest_path
#from pygraph.readwrite.dot import write

#__all__ = ['GNode', 'build_graph', 'print_align', 'print_cost',  'add_end_node', 'S']

S = {'a':{'a':2, 'c':1, 'g':2, 't':1, '-':1},
     'c':{'a':1, 'c':4, 'g':3, 't':2, '-':2},
     'g':{'a':2, 'c':3, 'g':1, 't':1, '-':3},
     't':{'a':1, 'c':2, 'g':1, 't':2, '-':1},
     '-':{'a':1, 'c':2, 'g':3, 't':1, '-':99}
     }

class GNode(object):
    def __init__(self, i, ch_i, j, ch_j):
        self.i, self.j = i, j
        self.ch_i, self.ch_j = ch_i, ch_j

    def __str__(self):
        return "(%d%s %d%s)" %(self.i, self.ch_i, self.j, self.ch_j)
    __repr__ = __str__

    def __hash__(self):
        # identify the node with the indexes of the chars in the 2 strings
        return hash((self.i, self.j, self.ch_i, self.ch_j))

    def __eq__(self, other):
        return hash(self) == hash(other)

class Graph(digraph):
    def get_node(self, i, j):
        for n in self.nodes():
            if (n.i == i) and (n.j == j):
                return n
        raise KeyError('Node (%d %d) not found!' %(i, j))

    def __init__(self, s1, s2):
        self.__s1 = s1
        self.__s2 = s2
        digraph.__init__(self)

        #def build_graph(s1, s2):
        #gr.parents = gr.incidents
        #gr.childs = gr.neighbors

        # useful for test on the whole graph
        tot_len = len(s1)+len(s2)
        s1_pad, s2_pad = s1[:], s2[:]
        while len(s1_pad) <= tot_len:
            s1_pad += '-'
        while len(s2_pad) <= tot_len:
            s2_pad += '-'

        # build all nodes
        for i, chi in enumerate(s1_pad):
            for j, chj in enumerate(s2_pad):
                # if we're out of both strings length we are comparing two gaps
                if (i <= len(s1) and j <= len(s2)):
                    # can't have more than len(s1) gaps in s2 and vice versa
                    if ((i >= j) and ((i-j) <= len(s1))) or ((i <= j) and ((j - i) <= len(s2))):
                        node = GNode(i, chi, j, chj)
                        self.add_node(node)

        # add the links between the nodes
        for n in self.nodes():
            for h, k in [(n.i+1, n.j), (n.i+1, n.j+1), (n.i, n.j+1)]:
                try:
                    nn = self.get_node(h, k)
                except KeyError, e:
                    pass
                else:
                    ## if we're comparing a gap, there is only one way to go
                    if (n.i >= len(s1) and (nn.i==n.i+1 and nn.j==n.j+1))\
                            or (n.j >= len(s2) and (nn.i==n.i+1 and nn.j==n.j+1)):
                        add_edge = True
                    elif (n.i < len(s1) and n.j < len(s2)):
                        # if we compare two chars every direction is possible
                        add_edge = True
                    else:
                        add_edge = False

                    if add_edge:
                        wt = self.weight(n, nn)
                        self.add_edge((n, nn), wt=wt)
                        #print 'Added link from %s to %s, wt %d' %(n, nn, wt)

    def weight(self, par, chl):
        # verify that par is the parent and chl the child
        if par.i > chl.i or par.j > chl.j:
            par, chl = chl, par
        # ottimizza "liane"
        # somma tutti i pesi degli archi dei percorsi "obbligati" del grafo
        if (chl.ch_i == '-'):
            partial = 0
            for j, chj in enumerate(self.__s2[chl.j:]):
                partial += S[chl.ch_i][chj]
            return partial
        elif (chl.ch_j == '-'):
            partial = 0
            for j, chi in enumerate(self.__s1[chl.i:]):
                partial += S[chl.ch_j][chi]
            return partial
        else:
            # altrimenti calcola il peso di una transizione semplice
            return self.weight_single_step(par, chl)

    def weight_single_step(self, par, chl):
        if par.i == chl.i:
            h = '-'
        else:
            h = par.ch_i
        if par.j == chl.j:
            k = '-'
        else:
            k = par.ch_j
        return S[h][k]

def get_align(steps):
    print steps
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
                # don't give error on the fake last node
                if (next_step.i, next_step.j) != (-1, -1):
                    print 'error:',step, next_step
    return s1, s2

def print_align(steps):
    s1, s2 = get_align(steps)
    print s1
    print s2

def get_cost(steps):
    s1, s2 = get_align(steps)
    cost = 0
    for c1, c2 in zip(s1, s2):
        cost += S[c1][c2]
    return cost

def print_cost(steps):
    cost = get_cost(steps)
    print 'Cost',cost

#def weight_single_step(par, chl):
#    if par.i == chl.i:
#        h = '-'
#    else:
#        h = par.ch_i
#    if par.j == chl.j:
#        k = '-'
#    else:
#        k = par.ch_j
#    return S[h][k]
#
#def weight_step(gr, par, chl):
#    # verify that par is the parent and chl the child
#    if par.i > chl.i or par.j > chl.j:
#        par, chl = chl, par
#    # ottimizza "liane"
#    #print chl, neighbors()
#    if (chl.ch_i == '-') or (chl.ch_j == '-'):
#        return
#    else:
#        return weight_single_step(par, chl)


def add_end_node(gr, s1, s2):
    end_node = GNode(-1, 'end', -1, 'end')
    gr.add_node(end_node)
    #real_end_nodes = [n for n in gr.nodes() if len(gr.neighbors(n))==0]
    #real_end_nodes = [n for n in gr.nodes() if (n.i >= len(s1)) and (n.j >= len(s2))]
    real_end_nodes = [n for n in gr.nodes() if (n.i >= len(s1)) or (n.j >= len(s2))]
    for n in real_end_nodes:
        gr.add_edge((n, end_node), wt=0)
    return end_node

