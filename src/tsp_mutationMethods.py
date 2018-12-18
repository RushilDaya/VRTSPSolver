import random 
import tsp_path2adj
import tsp_adj2path
import numpy as np
from mixins import _startAtOne

MAX_ITER = 1
INNER_MUT_PROB = 10

def get_MaxIter():
	return MAX_ITER

def set_MaxIter(value):
	MAX_ITER = value

def get_InnerMutProb():
	return INNER_MUT_PROB

def set_InnerMutProb(value):
	INNER_MUT_PROB = value

def mapping():
	function_mappings = {'tsp_inversion': tsp_inversion, 'tsp_swap': tsp_swap, 'tsp_nSwap': tsp_nSwap, 'tsp_insertion': tsp_insertion, 'tsp_scramble': tsp_scramble,'tsp_3scramble': tsp_3scramble}
	return function_mappings

def _selectRep(Chrom, REPRESENTATION):
	if REPRESENTATION == 'REP_PATH':
		return Chrom
	elif REPRESENTATION == 'REP_ADJACENCY':
		return tsp_adj2path.tsp_adj2path(Chrom)
	else:
		raise ValueError('Invalid representation provided')

def _returnRep(Chrom, REPRESENTATION):
	if REPRESENTATION == 'REP_PATH':
		return _startAtOne(Chrom)
	if REPRESENTATION == 'REP_ADJACENCY':
		return tsp_path2adj.tsp_path2adj(Chrom)

# low level operator to perform inversion mutation
def tsp_inversion(oldChrome, REPRESENTATION):
	# NOTE: inversion mutation always needs to be performed on path representation
	# old Chrome is an vector defining a single chromosome

	tempChrome = _selectRep(oldChrome,REPRESENTATION)

	cutLoci = np.sort(random.sample(range(len(tempChrome)), 2))
	
	tempChrome[cutLoci[0]:cutLoci[1]] = tempChrome[cutLoci[0]:cutLoci[1]][::-1]
	
	return _returnRep(tempChrome,REPRESENTATION)

# low level operator to perform swap mutation
def tsp_swap(oldChrome, REPRESENTATION):
	# NOTE: swap mutation always needs to be performed on path representation
	# old Chrome is an vector defining a single chromosome
	
	tempChrome = _selectRep(oldChrome,REPRESENTATION)
	
	x,y = random.sample(range(len(tempChrome)), 2)

	tempChrome[x],tempChrome[y]=tempChrome[y],tempChrome[x]
	
	return _returnRep(tempChrome,REPRESENTATION)

# low level operator to perform repeted swap mutation
def tsp_nSwap(oldChrome, REPRESENTATION):
	# Perform up to MAX_ITER swaps in the chromosome with a probability of ProbSwap

	tempChrome = _selectRep(oldChrome,REPRESENTATION)

	for i in range(MAX_ITER):
		x,y = random.sample(range(len(tempChrome)), 2)
		if random.random()<=INNER_MUT_PROB:
			tempChrome[x],tempChrome[y]=tempChrome[y],tempChrome[x]

	return _returnRep(tempChrome,REPRESENTATION)

# low level operator to perform insertion mutation
def tsp_insertion(oldChrome, REPRESENTATION):

	tempChrome = _selectRep(oldChrome,REPRESENTATION)
	x,y = random.sample(range(len(tempChrome)), 2)
	
	elm1 = tempChrome[x]

	tempChrome = np.insert(tempChrome,y,elm1)
	tempChrome = np.delete(tempChrome,x) if (x<y) else np.delete(tempChrome,x+1)

	return _returnRep(tempChrome,REPRESENTATION)

# low level operator to perform repeted scramble mutation
def tsp_scramble(oldChrome, REPRESENTATION):

	tempChrome = _selectRep(oldChrome,REPRESENTATION)
	x,y = np.sort(random.sample(range(len(tempChrome)), 2))

	tempChrome[x:y] = np.random.permutation(tempChrome[x:y])

	return _returnRep(tempChrome,REPRESENTATION)

# low level operator to perform repeted scramble mutation
def tsp_3scramble(oldChrome, REPRESENTATION):

	tempChrome = _selectRep(oldChrome,REPRESENTATION)
	
	for i in range(MAX_ITER):
		x = random.randrange(len(oldChrome)-1)
		y = x+2
		if random.random()<=INNER_MUT_PROB:
			tempChrome[x:y] = np.random.permutation(tempChrome[x:y])

	return _returnRep(tempChrome,REPRESENTATION)
