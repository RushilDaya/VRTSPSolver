import random 
import tsp_path2adj
import tsp_adj2path
import numpy as np
from mixins import _startAtOne

# low level operator to perform inversion mutation
def mapping():
	function_mappings = {'tsp_inversion': tsp_inversion,}
	return function_mappings

def tsp_inversion(oldChrome, REPRESENTATION):
	# NOTE: inversion mutation always needs to be performed on path representation
	# old Chrome is an vector defining a single chromosome

	if REPRESENTATION == 'REP_PATH':
		tempChrome = oldChrome
	elif REPRESENTATION == 'REP_ADJACENCY':
		tempChrome = tsp_adj2path.tsp_adj2path(oldChrome)
	else:
		raise ValueError('Invalid representation provided')

	cutLoci = np.sort(random.sample(range(0, len(tempChrome)-1), 2))
	# need to subtract because of how python indexes arrays
	# when you iterate in the reverse order.
	
	if cutLoci[0] == 0: # TODO: figure out a better way of dealing with this edge case
		tempChrome[cutLoci[0]:cutLoci[1]+1] = tempChrome[cutLoci[1]::-1]
	else:
		tempChrome[cutLoci[0]:cutLoci[1]+1] = tempChrome[cutLoci[1]:cutLoci[0]-1:-1]

	if REPRESENTATION == 'REP_PATH':
		return _startAtOne(tempChrome)
	if REPRESENTATION == 'REP_ADJACENCY':
		return tsp_path2adj.tsp_path2adj(tempChrome)