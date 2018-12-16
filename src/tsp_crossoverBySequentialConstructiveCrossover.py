import numpy as np 
import random
from mixins import  _rangedSet

MATRIX = np.matrix([[0, 10, 2.5, 2],
                    [10, 0, 2, 2.5],
                    [2.5, 2, 0, 3],
                    [2, 2.5, 3, 0]])

PARENTS = [[1,2,3,4],[1,3,2,4]]

def _chooseNext(parentList, lastChildNode, unvistedNodes):
    # will return the first legitimate node in the parentList occuring after the lastChildNode ( in the Parent )
    # if none are found it will return the /left most/ ie smallest child  in the unvisitedNode list 
    startIndex = parentList.index(lastChildNode)
    for i in range(startIndex+1, len(parentList)):
        if parentList[i] in unvistedNodes:
            return parentList[i]

    return min(unvistedNodes)

def _selectNearest(fromNode, optionsArray, distanceMatrix):
    # returns the node in the optionsArray which is closer to the fromNode
    distances=[]
    for i in range(len(optionsArray)):
        distances.append(distanceMatrix[fromNode-1,optionsArray[i]-1]) # zero indexed matrix but nodes are 1 indexed
    
    indexOfNearest = distances.index(min(distances))
    return optionsArray[indexOfNearest]

def tsp_crossoverBySequentialConstructiveCrossover(parents, distanceMatrix):
    # the parents is a 2-by-NVAR matrix
    # distanceMatrix is NVAR-by-NVAR matrix
    # the distance matrix should be read as if its one indexed wrt cities

    # do a check to make sure both paths start at 1
    if parents[0][0] != 1 or parents[1][0] != 1:
        raise AttributeError('One or More parent paths don\'t start at 1')

    # initialize the objects 
    NVAR = len(parents[0])
    unvisitedNodes = _rangedSet(NVAR)
    child = []
    child.append(1)
    unvisitedNodes.remove(1)

    for i in range(1,NVAR):
        parentOneNextNode = _chooseNext(parents[0],child[i-1], unvisitedNodes) 
        parentTwoNextNode = _chooseNext(parents[1],child[i-1], unvisitedNodes)
        selectedNextNode = _selectNearest(child[i-1],[parentOneNextNode,parentTwoNextNode],distanceMatrix) 
        child.append(selectedNextNode)
        unvisitedNodes.remove(selectedNextNode)

    if len(child) != NVAR:
        raise RuntimeError('SCX performed badly')
    if len(unvisitedNodes) != 0:
        raise RuntimeError('SCX performed badly')

    return child

    
if __name__ == '__main__':
    print(tsp_crossoverBySequentialConstructiveCrossover(PARENTS,MATRIX))