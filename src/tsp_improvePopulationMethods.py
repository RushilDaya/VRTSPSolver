import numpy as np 
import tsp_swapSubpath
from mixins import _startAtOne

# all these methods assume path representation

def mapping():
	function_mappings = {'tsp_none': tsp_none, 'tsp_improvePath':tsp_improvePath}
	return function_mappings


def tsp_none(path, Dist=None):
    # used when heuristic is not wanted
    return path

def tsp_improvePath(path,Dist=None):
    ncities = len(path)
    maxlen = min(3, ncities/2)
    for length in range(1, maxlen):
        for start in range(ncities):
            stop = np.mod((start+length),ncities)
            idx1 = np.mod((start + ncities-1),ncities)
            idx2 = np.mod((stop+1),ncities)
            gain = Dist[path[idx1]-1,path[start]-1] + Dist[path[stop]-1,path[idx2]-1]- Dist[path[idx1]-1,path[stop]-1] - Dist[path[start]-1,path[idx2]-1]           
            if (gain > 0):
                path = tsp_swapSubpath.tsp_swapSubpath(ncities, path[:], start, length)
    
    return _startAtOne(path).tolist()