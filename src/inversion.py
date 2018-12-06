# low level operator to perform inversion mutation

import numpy as np
import random 
from path2adj import path2adj
from adj2path import adj2path

def inversion(oldChrome,REP='adjacency'):
    # old Chrome is an vector defining a single chromosome

    if REP = 'path':
        tempChrome = oldChrome
    else if REP == 'adjaceny':
        tempChrome = adj2path(oldChrome)
    else:
        raise ValueError('Invalid representation provided')

    cutLoci = np.sort(random.sample(range(0, len(tempChrome)), 2))
    # need to subtract because of how python indexes arrays
    # when you iterate in the reverse order.
    tempChrome[cutLoci[0]:cutLoci[1]] = tempChrome[cutLoci[1]-1:cutLoci[0]-1:-1]


    if REP == 'path':
        return tempChrome
    if REP == 'adjacency':
        return path2adj(tempChrom)