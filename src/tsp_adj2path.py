# adj2path (Adj)
# takes in a numpy array in the adjacency rep
# returns a numpy array in the path rep.

import numpy as np
from tsp_exceptions import InvalidCycleError

def tsp_adj2path(adjacencyArray, subCycleDetection=False):
	# note that python arrays are zero indexed the TSP representations
	# assume one indexed nodes.

	# if subCycleDetection is true an exception will be thrown in
	# the case of the presence of sub-cycles A-B-C D-E
	visitedNodes = set()

	pathLength = len(adjacencyArray)
	pathArray = np.zeros(pathLength, dtype='i')
	pathArray[0] = 1 # always start at the first node for consistency
	walkingIndex = 0

	for i in range(pathLength-1):

		try:
			nextNode = adjacencyArray[walkingIndex]
		except IndexError:
			raise InvalidCycleError("provided adjacency representation is invalid")

		if subCycleDetection and nextNode in visitedNodes:
			raise InvalidCycleError("provided adjacency representation contains cycles")

		pathArray[i+1] = nextNode
		walkingIndex = nextNode -1
		visitedNodes.add(nextNode)

	return pathArray
