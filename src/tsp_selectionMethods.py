import numpy as np
import random

def mapping(REP):
	if(REP=='REP_ADJACENCY'):
		function_mappings = {'tsp_sus': tsp_sus,}
		return function_mappings
	else:
		return None

def _getTrailIndex(TrailVal,FitnessSpan):
	return len([ True for item in FitnessSpan if item < TrailVal ])

def tsp_sus(FitnV,Nsel):
	# perform stochastic universal sampling
	Nind = len(FitnV)
	cumfit =  np.cumsum(FitnV)
	stride = cumfit[Nind-1]/Nsel
	randV = random.random()*stride
	trails = np.linspace(0, stride*(Nsel-1), num=Nsel) + randV
	selectedIndices = [_getTrailIndex(item, cumfit) for item in trails]
	np.random.shuffle(selectedIndices) # in-place function
	return np.array(selectedIndices)