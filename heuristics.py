
from pygraph.algorithms.minmax import heuristic_search

from common_graph import *

#
# heuristic 1
#
# BAD
def minimum_residual_cost(node, end, s1, s2):
    """
    compute heuristic based on the minumin cost based on
    the chars in the residual strings
    """
    if node == end:
        return 0
    # caratteri da rimuovere, inizio prendendoli tutti e poi tolgo man mano
    # i caratteri che compaiono nelle due sottostringhe
    chars = ['a', 'c', 'g', 't', '-']
    hs1 = s1[node.i:]
    hs2 = s2[node.j:]
    if hs2 == '' or hs1 == '':
        # no decisions left
        return 0
    hs = hs1[:]+hs2[:]
    for ch in hs:
        if ch in chars:
            chars.remove(ch)
    # chars now are the characters that don't show in the remaining strings
    S_red = S.copy()
    for k in S_red.keys():
        S_red[k] = S[k].copy()
        #S_red[k].pop(k)
    #for ch in chars:
    #    S_red.pop(ch)
    ##for k in S_red.keys():
    #    for ch in chars:
    #        S_red[k].pop(ch)
    all_costs = []
    for k in S_red.keys():
        all_costs += S_red[k].values()
    if len(all_costs) == 0:
        # end reached
        return 0
    #heust =  min(all_costs)*(len(s1) - node.i + len(s2) - node.j)
    heust = min(all_costs)*min([len(hs1), len(hs2)])
    return heust

#
# heuristic 2
#

def _scorr(s1, s2):
    corr = 0
    # pad s1
    tmps1 = '-'*len(s2)+s1[:]+'-'*len(s2)
    for step in range(len(tmps1)-len(s2)):
        tmps2 = '-'*step+s2[:]
        for i, c in enumerate(tmps2):
            if c != '-' and c == tmps1[i]:
                corr += 1
    return corr


def _scorr2(s1, s2):
    #corr = 0
    corrs = []
    # pad s1
    tmps1 = '-'*len(s2)+s1[:]+'-'*len(s2)
    for step in range(len(tmps1)-len(s2)):
        tmps2 = '-'*step+s2[:]
        corr = 0
        # count only differing chars at every shift
        for i, c in enumerate(tmps2):
            #if c != '-' and c == tmps1[i]:
            if c != tmps1[i]:
                # cost?
                corr += 1
        corrs.append(corr)
    if corrs:
        return min(corrs)
    else:
        return 0

def string_correlation(node, end, s1, s2):
    """
    compute a correlation between the residual strings,
    normalized to the correlation of the 2 initial strings to have a feasible heuristic
    """
    if node == end:
        # necessary because we assume end node with indexes -1, -1
        return 0
    ref = _scorr(s1, s2)
    hs1 = s1[node.i:]
    hs2 = s2[node.j:]
    cur = _scorr(hs1, hs2)
    #print node, hs1, hs2,  cur, ref
    h = cur/float(ref)
    return h

#
# utilities
#

hlist = {'mrc':minimum_residual_cost,
         'sc':string_correlation,
         # fake heuristic
         'none':lambda n, e, s1, s2: 0
         }

def get_h(name, *args, **kw):
    """
    build a function that can be used to compute the heuristic.
    The heuristic may need other parameters than the current node and the
    end node, they must be passed here in addiction to the name
    """
    func = hlist[name]
    def h(node, end):
        h_cost = func(node, end, *args)
        if kw.get('cmp', None):
            # allow to compare an heuristic with the real distance
            gr = kw.get('gr')
            ret = heuristic_search(gr, node, end, get_h('none', *args))
            real_cost = get_cost(ret)
            print node, 'Heuristic cost:', h_cost, 'Real cost:',real_cost
            if h_cost > real_cost:
                print 'BAD H'
        return h_cost
    return h

