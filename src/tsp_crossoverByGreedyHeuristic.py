import numpy as np 
import random

MATRIX = np.matrix([[0,1,1],
                    [1,0,1],
                    [1,1,0]])
PARENTS = np.matrix([[2,3,1],
                     [3,1,2]])

def _reverse(adjList):
	#  returns the adjacency representation of walking through
	# the nodes in the reversed order 
	return np.argsort(adjList)+1

def _rangedSet(rangeSize):
	# returns a set thats of 1-indexed values
	# eg if rangeSize is 5 the returned set is {1,2,3,4,5}
	return set (np.linspace(1,rangeSize,rangeSize).astype('int'))

def _getDistance(fromNode, toNode, distanceMatrix):
    # the nodes are 1 indexed here
    return distanceMatrix[fromNode-1,toNode-1]

def tsp_crossoverByGreedyHeuristic(parents, distanceMatrix):
    # the parents is a 2-by-NVAR matrix
    # distanceMatrix is NVAR-by-NVAR matrix
    # the distance matrix should be read as if its one indexed wrt cities
    # but remember that when actually indexing in python it uses zero-indices

    # initialize the objects 
    (_,NVAR) = parents.shape
    unvistedNodes = _rangedSet(NVAR)
    child = np.zeros(NVAR)
    reversedParent1 = _reverse(parents[0])
    reversedParent2 = _reverse(parents[1])

    adjacencyList = parents.tolist() # there is probably a more efficient way to do this
    adjacencyList.append(reversedParent1)
    adjacencyList.append(reversedParent2)
    adjacencyMatrix = np.transpose(np.matrix(adjacencyList))


    # start in a random city
    selectedNode = random.randint(0,NVAR-1)
    startNode = selectedNode
    vistedNodes.add(selectedNode)
    unvistedNodes.remove(selectedNode)

    while len(unvistedNodes) > 0:
        # determine the the available options
        candidateNextNodes = adjacencyMatrix[selectedNode-1]
        validCandidates = []
        for candidate in candidateNextNodes:
            if candidate in unvistedNodes:
                validCandidates.append(candidate)
        
        if len(validCandidates) == 0:
            # no unvisited nodes pick at random
            selectedNextNode = random.choice(tuple(unvisitedNodes))
        else:
            candidateDistances = [_getDistance(selectedNode,candidate,distanceMatrix) for candidate in validCandidates]
            selectedNextNode = validCandidates[candidateDistances.argmax()]

        # visit the node
        child[selectedNode] = selectedNextNode
        unvistedNodes.remove(selectedNextNode)
        selectedNode = selectedNextNode
    
    child[selectedNode] = startNode # close the loop

    return child

    


if __name__ == '__main__':
    tsp_heuristicCrossover(PARENTS,MATRIX)