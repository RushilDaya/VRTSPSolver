import numpy as np
import tsp_adj2path
import tsp_path2adj
import tsp_improveMethods

# This function improves a tsp population by removing local loops from each individual.

def tsp_improvePopulation(REPRESENTATION, IMPROVE_FUNC, Chrom, DISTANCE_MATRIX):

	ChromList = Chrom.tolist()
	newChrom = []
	for i in range(len(ChromList)):
		if REPRESENTATION == 'REP_PATH':
			temp = ChromList[i]
		elif REPRESENTATION == 'REP_ADJACENCY':
			temp = tsp_adj2path.tsp_adj2path(ChromList[i])

		improved = IMPROVE_FUNC(temp, DISTANCE_MATRIX)

		if REPRESENTATION == 'REP_PATH':
			newChrom.append(improved)
		elif REPRESENTATION == 'REP_ADJACENCY':
			newChrom.append(tsp_path2adj.tsp_path2adj(improved))
	return np.matrix(newChrom)
