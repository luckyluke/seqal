#!/usr/bin/env python

"""
Implementation of sequence alignment using A*
"""

class Node(object):
    def __init__(self, i, j, s1, s2, parent=None):
        # indexes of the 2 chars identifying the node
        self.i, self.j = i, j
        # the 2 strigns of reference
        self.s1, self.s2 = s1, s2
        # parent node
        self.parent = parent
        # node reached inserting a gap on the 1st string
        self.sub_before = None
        # node reached if no gap is inserted
        self.sub_keep = None
        # node reached inserting a gap on the 2 string
        self.sub_after = None

    def ends_align(self):
        """ Return True if the node is the last one for an alignment """
        return self.s1[self.i] == '-' and self.s2[self.j] == '-'
        #return False

    def estimate_dist_goal(self):
        """
        The h() function.

        Estimate distance from the end of the alignment, based on the number
        of remaining characters to compare.
        """
        # FIXME: counts even trailing '-'
        return len(self.s1) - self.i - 1 + len(self.s2) - self.j -1

    def childs(self):
        """ return list of child nodes, build them if necessary """
        self.sub_before = Node(self.i, self.j+1, self.s1, self.s2)
        self.sub_keep = Node(self.i+1, self.j+1, self.s1, self.s2)
        self.sub_after = Node(self.i+1, self.j, self.s1, self.s2)
        return [self.sub_before, self.sub_keep, self.sub_after]

    def reconstruct_path(self):
        if self.parent:
            p = self.parent.reconstruct_path()
            p.append(self)
            return p
        else:
            return []

    def __str__(self):
        #return '%d %d %s' %(self.i, self.j, hash(self))
        return '%d %d %d' %(self.i, self.j, self.estimate_dist_goal())
        #return '%d %d b(%s) k(%s) a(%s)' %(self.i, self.j, self.sub_before, self.sub_keep, self.sub_after)
    __repr__ = __str__

    # methods needed to be meaningful elements of sets
    def __hash__(self):
        # identify the node with the indexes of the chars in the 2 strings
        return hash((self.i, self.j))

    def __eq__(self, other):
        return hash(self) == hash(other)

# cost matrix
S = {'a':{'a':0, 'c':1, 'g':2, 't':1, '-':1},
     'c':{'a':1, 'c':0, 'g':3, 't':2, '-':2},
     'g':{'a':2, 'c':3, 'g':0, 't':1, '-':3},
     't':{'a':1, 'c':2, 'g':1, 't':0, '-':1},
     '-':{'a':1, 'c':2, 'g':3, 't':1, '-':99},
     }
def dist(par, ch):
    if par.i == ch.i:
        h = '-'
    else:
        h = par.s1[par.i]
    if par.j == ch.j:
        k = '-'
    else:
        k = par.s2[par.j]
    return S[h][k]

# see http://it.wikipedia.org/wiki/A*#Pseudo_Codice
def a_star(s1, s2):
    """ find optimum alignment using A* """
    print s1,s2
    closed_set, open_set = set(), set()
    g_score, h_score, f_score = {}, {}, {}
    start_node = Node(0, 0, s1, s2)

    open_set.add(start_node)
    g_score[start_node] = 0
    h_score[start_node] = start_node.estimate_dist_goal()
    f_score[start_node] = h_score[start_node]

    while open_set:
        x = min(open_set, key=f_score.get)
        print x.i,x.j
        print 'open',open_set
        print 'closed',closed_set
        if not x.ends_align():
            open_set.remove(x)
            closed_set.add(x)

        if len(open_set) == 1 and open_set[0].ends_align():
            # optimum alignment found!!!
            return open_set[0].reconstruct_path()

        for y in x.childs():
            if y in closed_set:
                continue

            # posso fare x - y TODO
            y_g_score = g_score[x] + dist(x, y)
            if y not in open_set:
                open_set.add(y)
                y_better = True

            elif y_g_score < g_score[y]:
                y_better = True

            else:
                y_better = False

            if y_better:
                y.parent = x
                g_score[y] = y_g_score
                h_score[y] = y.estimate_dist_goal()
                f_score[y] = g_score[y] + h_score[y]

            #else:
            # TODO:remove y from x's childs?

    # impossibile?????
    raise Exception('Failure')

def prepare_strings(s1, s2):
    # longest string always s1
    if len(s2) > len(s1):
        s1, s2 = s2, s1

    # pad the shortest string
    for i in range(len(s1)-len(s2)):
        s2 += '-'
    
    # add trailing gap to easy recognise ends of alignment
    s1 += '-'
    s2 += '-'

    return s1.lower(), s2.lower()

s1 = 'tccg'
s2 = 'ta'

if __name__=='__main__':

    a_star(*prepare_strings(s1, s2))

