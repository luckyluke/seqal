#!/usr/bin/env python

"""
Implementation of sequence alignment using A*
"""
import sys
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
        #return self.s1[self.i] == '-' and self.s2[self.j] == '-'
        return (self.i>=len(self.s1) and self.j>=len(self.s2))
        #return (self.i==len(self.s1) and self.j==len(self.s2))
        #return False

    def estimate_dist_goal(self):
        """
        The h() function.

        Estimate distance from the end of the alignment, based on the number
        of remaining characters to compare.
        """
        s1_n_chars = len(self.s1.replace('-', ''))
        s2_n_chars = len(self.s2.replace('-', ''))
        dist = 0
        if self.i < s1_n_chars:
            dist += s1_n_chars - self.i - 1
        if self.j < s2_n_chars:
            dist += s2_n_chars - self.j - 1
        return dist
        #return 0
        #return 99*(s1_n_chars+s2_n_chars-self.i-self.j)
        
        
    def childs(self):
        """ return list of child nodes, build them if necessary """
        self.sub_before = Node(self.i, self.j+1, self.s1, self.s2)
        #self.sub_before.cost=dist(self,self.sub_before)
        self.sub_keep = Node(self.i+1, self.j+1, self.s1, self.s2)
        #self.sub_keep.cost=dist(self,self.sub_keep)
        self.sub_after = Node(self.i+1, self.j, self.s1, self.s2)
        #self.sub_after.cost=dist(self,self.sub_after)

        if self.ends_align():
            return []
        else:
            return [self.sub_before, self.sub_keep, self.sub_after]

    def reconstruct_path(self):
        if self.parent:
            p = self.parent.reconstruct_path()
            p.append(self)
            return p
        else:
            p=[]
            p.append(self)
            return p

    def __str__(self):
        #return '%d %d %s' %(self.i, self.j, hash(self))
        return '%d %d %d' %(self.i, self.j, self.estimate_dist_goal())
        #return '(%d,%d)' %(self.i, self.j)
        #return '%d %d b(%s) k(%s) a(%s)' %(self.i, self.j, self.sub_before, self.sub_keep, self.sub_after)
        #if self.i<len(self.s1) and self.j<len(self.s2):
        #    return '(%s[%d],%s[%d])' %(self.s1[self.i],self.i,self.s2[self.j],self.j)
        #elif self.i<len(self.s1) and self.j>=len(self.s2):
        #    return '(%s[%d],-[%d])' %(self.s1[self.i],self.i,self.j)
        #elif self.i>=len(self.s1) and self.j<len(self.s2):
        #    return '(-[%d],%s[%d])' %(self.i,self.s2[self.j],self.j)        
        #else:
        #    return '(-[%d],-[%d])' %(self.i,self.j)
    __repr__ = __str__

    # methods needed to be meaningful elements of sets
    def __hash__(self):
        # identify the node with the indexes of the chars in the 2 strings
        return hash((self.i, self.j))

    def __eq__(self, other):
        return hash(self) == hash(other)

# cost matrix
S = {'a':{'a':0, 'c':1, 'g':2, 't':1, '-':1},
     'c':{'a':1, 'c':0, 'g':15,'t':1, '-':2},
     'g':{'a':2, 'c':15,'g':0, 't':1, '-':1},
     't':{'a':1, 'c':1, 'g':1, 't':0, '-':1},
     '-':{'a':1, 'c':2, 'g':1, 't':1, '-':99}
     }
def dist(par, ch):

    if par.i == ch.i:
        h = '-'
    else:
        if par.i<len(par.s1):
            h = par.s1[par.i]
        else:
            h = '-'
    if par.j == ch.j:
        k = '-'
    else:
        if par.j<len(par.s2):
            k = par.s2[par.j]
        else:
            k = '-'
    return S[h][k]

# see http://it.wikipedia.org/wiki/A*#Pseudo_Codice
def a_star(s1, s2):
    """ find optimum alignment using A* """
    closed_set, open_set = set(), set()
    g_score, h_score, f_score = {}, {}, {}
    start_node = Node(0, 0, s1, s2)

    open_set.add(start_node)
    g_score[start_node] = 0
    h_score[start_node] = start_node.estimate_dist_goal()
    f_score[start_node] = h_score[start_node]
    
    while open_set:
        x = min(open_set, key=f_score.get)
        
        print    "\n\n----------------------"
        print    "open_set: ", open_set
        print    "----------------------"
        print    "closed_set: ",closed_set
        print    "----------------------"
        print    "current node: ",x
        print    "g_score[y]: ",g_score[x]
        print    "h_score[y]: ",h_score[x]
        print    "f_score[y]: ",f_score[x]
        print    "----------------------"

        #remove/add lowest cost node from open_set/closed_set and use it as current node
        open_set.remove(x)
        closed_set.add(x)
        
        print    "open_set: ", open_set
        print    "----------------------"
        print    "closed_set: ",closed_set        
        print    "----------------------"
        
        print "Currently processing %d total nodes. len(OPEN_SET)=%d. len(CLOSED_SET)=%d" %((len(open_set)+len(closed_set)),len(open_set),len(closed_set))
        
        #goal test
        if x.ends_align():
            print "\n\nGOAL NODE!\n\nSUBSTITUTION COST: %d" %(g_score[x])
            return x.reconstruct_path()
        
        
        
        #expand his child nodes and pushes them into open_set
        for y in x.childs():
            #we need to check if child node has previously been tested
            #because we are expanding a graph instead of a tree
            y_g_score = g_score[x] + dist(x, y)
            print    "\n%s ---> %s" %(x,y)
            if y in closed_set:
                print    y, " was in closed_set. This child will be ignored."
                continue
            
            if y not in open_set:
                print    y, " wasn't in open_set. I add it."
                open_set.add(y)
                y_better = True

            elif y_g_score <= g_score[y]:
                print    y, " was in open_set. This new is better than old node."
                y_better = True

            else:
                print    y, " is worst. This child will be ignored."
                y_better = False
                
            if y_better:
                print "vecchio padre"
                print y.parent
                y.parent = x
                print "ho aggiornato il padreeeeeee!!"
                print x
                print y.parent
                g_score[y] = y_g_score
                h_score[y] = y.estimate_dist_goal()
                f_score[y] = g_score[y] + h_score[y]
                print    "\ng_score[y]: ",g_score[y]
                print    "h_score[y]: ",h_score[y]
                print    "f_score[y]: ",f_score[y]
            else:
                print    "\ng_score[y]: ",y_g_score
                print    "h_score[y]: ",y.estimate_dist_goal()
                print    "f_score[y]: ",y_g_score+y.estimate_dist_goal()

        #sys.stdin.read(1)
        
        
    # impossibile?????
    raise Exception('Failure')
    
def prepare_strings(s1, s2):
    # longest string always s1
    if len(s2) > len(s1):
        s1, s2 = s2, s1

    # pad the shortest string
    #for i in range(len(s1)-len(s2)):
    #    s2 += '-'
    
    # add trailing gap to easy recognise ends of alignment
    #s1 += '-'
    #s2 += '-'

    return s1.lower(), s2.lower()

#s1 = 'cttagagcacggccgcccccgatatatat'
#s2 = 'gccccaagagaggccccgatatgcgatat'
s1 = 'cagata'
s2 = 'taggata'
#s1="g"
#s2="c"

if __name__=='__main__':
    print "-----------------"
    print "ALIGNMENT  BEGIN:"
    print "-----------------"
    o = a_star(*prepare_strings(s1, s2))
    ns1=''
    ns2=''
    for i in range(0,len(o)-1):
        if o[i].i == o[i+1].i:
            ns1+='-'
        else:
            if o[i].i<len(o[i].s1):
                ns1+=o[i].s1[o[i].i]
            else:
                ns1+='-'
        if o[i].j == o[i+1].j:
            ns2+='-'
        else:
            if o[i].j<len(o[i].s2):
                ns2+=o[i].s2[o[i].j]
            else:
                ns2+='-'
    print "\n-----------------"        
    print "END OF ALIGNMENT:"
    print "-----------------"
    print o[0].s1
    print o[0].s2
    print "-----------------"
    print ns1
    print ns2
    print "-----------------"

