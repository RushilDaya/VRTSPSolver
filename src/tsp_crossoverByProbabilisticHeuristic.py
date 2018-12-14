import numpy as np 
import random


MATRIX = np.matrix([[0, 1, 2.5, 2],
                    [1, 0, 2, 2.5],
                    [2.5, 2, 0, 3],
                    [2, 2.5, 3, 0]])

PARENTS = np.matrix([[4,1,2,3],
                     [4,3,1,2]])

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

def _probChoice(distances):
    # note return an random index of the distance array with a preference for nearest 
    # there are many ways we could do this selection
    # presented here is a very simplistic way more complex methods can be
    # explored if this is found to be a promising method
    # -------
    # 1) the same edge can appear multiple times: this should boost the probability of that edge being selected
    # 2) should use rankings and not actual distances: the actual distances may be very large and not very different from each other
    # -------

    distanceArray = np.array(distances)
    ranking = np.argsort(np.argsort(-distanceArray)) + 1 # having a zero item doesn't correctly work in the cumsum
    preferenceVector = np.cumsum(ranking) 
    maximum = preferenceVector[-1]
    randomSelection = random.random()*maximum
    
    for i in range(len(preferenceVector)):
        if randomSelection < preferenceVector[i]:
            return distanceArray[i]
    
    raise RuntimeError('function failed to determine an appropriate value')


def tsp_crossoverByProbabilisticHeuristic(parents, distanceMatrix):
    # the parents is a 2-by-NVAR matrix
    # distanceMatrix is NVAR-by-NVAR matrix
    # the distance matrix should be read as if its one indexed wrt cities
    # but remember that when actually indexing in python it uses zero-indices

    # initialize the objects 
    (_,NVAR) = parents.shape
    unvisitedNodes = _rangedSet(NVAR)
    child = np.zeros(NVAR)
    reversedParent1 = _reverse(parents[0]).tolist()[0]
    reversedParent2 = _reverse(parents[1]).tolist()[0]

    adjacencyList = parents.tolist() # there is probably a more efficient way to do this
    adjacencyList.append(reversedParent1)
    adjacencyList.append(reversedParent2)
    adjacencyMatrix = np.matrix(adjacencyList).transpose()


    # start in a random city
    selectedNode = random.randint(1,NVAR-1)
    startNode = selectedNode
    unvisitedNodes.remove(selectedNode)


    while len(unvisitedNodes) > 0:
        # determine the the available options

        candidateNextNodes = adjacencyMatrix[selectedNode-1]
        validCandidates = []
        for candidate in candidateNextNodes.tolist()[0]:
            if candidate in unvisitedNodes:
                validCandidates.append(candidate)


        if len(validCandidates) == 0:
            # no unvisited nodes pick at random
            selectedNextNode = random.choice(tuple(unvisitedNodes))
        else:
            candidateDistances = [_getDistance(selectedNode,candidate,distanceMatrix) for candidate in validCandidates]
            # ONLY DIFFERENCE to greedy crossover is here
            # instead of always picking the nearest we pick a random node
            # with preference for closer nodes
            indexOfSelection = _probChoice(candidateDistances)
            selectedNextNode = validCandidates[indexOfSelection]

        # visit the node
        child[selectedNode-1] = selectedNextNode
        unvisitedNodes.remove(selectedNextNode)
        selectedNode = selectedNextNode
    
    child[selectedNode-1] = startNode # close the loop
    return [int(item) for item in child]

    


if __name__ == '__main__':
    print(tsp_crossoverByGreedyHeuristic(PARENTS,MATRIX))