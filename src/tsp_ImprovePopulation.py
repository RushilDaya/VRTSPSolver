import numpy as np

# This function improves a tsp population by removing local loops from
# each individual.

def tsp_ImprovePopulation(popsize, ncities, pop, improve, dists):

if improve:
	for idx in range(popsize):
		result = improve_path(ncities, adj2path(pop(idx)), dists)
		pop(idx) = path2adj(result)

return pop