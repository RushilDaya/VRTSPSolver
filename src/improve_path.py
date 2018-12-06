import numpy as np

# This function improves a single tsp path in path representation by removing
# local loops up to pathlength 3.

def improve_path (ncities, path, Dist):
	
	maxlen =  min(3, ncities//2)

	for length in range(1,maxlen):
		for start in range(ncities):
			stop = np.mod((start + length),ncities)
			idx1 = np.mod((start + ncities-1),ncities)
			idx2 = np.mod((stop+1),ncities)
			gain = Dist(path(idx1),path(start)) + Dist(path(stop),path(idx2) - Dist(path(idx1),path(stop)) - Dist(path(start),path(idx2))
		if (gain > 0):
			path = SwapSubpath(ncities, path, start, length)
return path