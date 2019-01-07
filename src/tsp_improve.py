import numpy as np
import tsp_adj2path
import tsp_path2adj
import tsp_fun
import tsp_improveMethods

# This function improves a tsp population by removing local loops from each individual.

def tsp_improvePopulation(REPRESENTATION, IMPROVE_FUNC, Chrom, DISTANCE_MATRIX):
	ObjV = tsp_fun.tsp_fun(REPRESENTATION,Chrom,DISTANCE_MATRIX)
	sObjVArgs = np.argsort(ObjV)
	ChromList = Chrom.tolist()
	newChrom = []
	for i in range(len(ChromList)):
	#for idx, i in enumerate(sObjVArgs):
		if i in sObjVArgs[:10]:
			if REPRESENTATION == 'REP_PATH':
				temp = ChromList[i]
			elif REPRESENTATION == 'REP_ADJACENCY':
				temp = tsp_adj2path.tsp_adj2path(ChromList[i])

			improved = IMPROVE_FUNC(temp.tolist(), DISTANCE_MATRIX)

			if REPRESENTATION == 'REP_PATH':
				newChrom.append(improved)
			elif REPRESENTATION == 'REP_ADJACENCY':
				newChrom.append(tsp_path2adj.tsp_path2adj(improved))
		else:
			newChrom.append(ChromList[i])
	return np.matrix(newChrom)
