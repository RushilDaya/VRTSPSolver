import numpy as np
import tsp_adj2path
import tsp_improvePath

# This function improves a tsp population by removing local loops from
# each individual.

def tsp_improvePopulation(popsize, ncities, pop, improve, dists):

	if improve:
		for idx in range(popsize):
			result = tsp_improvePath(ncities, adj2path(pop(idx)), dists)
			pop[idx] = tsp_adj2path.tsp_adj2path(result)
	return pop