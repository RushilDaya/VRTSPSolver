# takes in a numpy array in the path rep
# returns a numpy array in the adjacency rep.

import numpy as np
from tsp_exceptions import InvalidCycleError


def tsp_path2adj(pathArray, subCycleDetection=False):
	# note that python arrays are zero indexed the TSP representations
	# assume one indexed nodes.

	# generating an adjacency representation from an invalid path will
	# result in a junk adjacency representation as well
	visitedNodes = set()
	if subCycleDetection:
		for node in path:
			if node in visitedNodes:
				raise InvalidCycleError("the provided path representation contains one or more subcyles")
			visitedNodes.add(node)


	pathLength = len(pathArray)
	adjacencyArray = np.zeros(pathLength, dtype='i')
	for i in range(pathLength-1):
		adjacencyArray[pathArray[i]-1] = pathArray[i+1] 
	adjacencyArray[pathArray[pathLength-1]-1] = pathArray[0] #close the loop

	return adjacencyArray