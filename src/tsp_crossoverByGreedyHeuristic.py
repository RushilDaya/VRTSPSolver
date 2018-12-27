import numpy as np 
import random
from mixins import _reverse, _rangedSet


MATRIX = np.matrix([[0, 1, 2.5, 2],
                    [1, 0, 2, 2.5],
                    [2.5, 2, 0, 3],
                    [2, 2.5, 3, 0]])

PARENTS = [[4,1,2,3],[4,3,1,2]]

def _getDistance(fromNode, toNode, distanceMatrix):
    # the nodes are 1 indexed here
    return distanceMatrix[fromNode-1,toNode-1]

def tsp_crossoverByGreedyHeuristic(parents, distanceMatrix):
    # the parents is a 2-by-NVAR matrix
    # distanceMatrix is NVAR-by-NVAR matrix
    # the distance matrix should be read as if its one indexed wrt cities
    # but remember that when actually indexing in python it uses zero-indices

    # initialize the objects 
    NVAR = len(parents[0])
    unvisitedNodes = _rangedSet(NVAR)
    child = np.zeros(NVAR)
    reversedParent1 = _reverse(parents[0])
    reversedParent2 = _reverse(parents[1])

    adjacencyList = parents
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
            indexOfNearest = candidateDistances.index(min(candidateDistances))
            selectedNextNode = validCandidates[indexOfNearest]

        # visit the node
        child[selectedNode-1] = selectedNextNode
        unvisitedNodes.remove(selectedNextNode)
        selectedNode = selectedNextNode
    
    child[selectedNode-1] = startNode # close the loop
    return [int(item) for item in child]

    


if __name__ == '__main__':
    print(tsp_crossoverByGreedyHeuristic(PARENTS,MATRIX))