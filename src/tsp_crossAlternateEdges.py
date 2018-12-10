import random
import numpy as np

def _reverse(adjList):
    #  returns the adjacency representation of walking through
    # the nodes in the reversed order 
    return np.argsort(adjList)+1

def _rangedSet(rangeSize):
    # returns a set thats of 1-indexed values
    # eg if rangeSize is 5 the returned set is {1,2,3,4,5}
    return set (np.linspace(1,rangeSize,rangeSize).astype('int'))

def _deterministicNewNode(parents,parentsReversed,parentIndex,walkingIndex,direction=0):
    if direction == 0:
        # note walking index here is zero indexed but the resulting
        # new node is not
        newNode = parents[parentIndex][walkingIndex]
    elif direction == 1:
        newNode = parentsReversed[parentIndex][walkingIndex]
        
    return newNode
            

def tsp_crossAlternateEdges(parents):
    # parents is a list with 2 chromosomes
    # performs the actual crossover assuming
    # adjacency representation
    
    # generate the parents in a reversed order
    parentsReversed = []
    parentsReversed.append(_reverse(parents[0]))
    parentsReversed.append(_reverse(parents[1]))
    
    visitedNodes = set()
    unvisitedNodes = _rangedSet(len(parents[0]))
    startingNode = random.randint(0,len(parents[0])-1)
    child = np.zeros(len(unvisitedNodes),dtype='int')
    walkingIndex = startingNode
    parentIndex = 0 # will either be 0 or 1 indicing which parent to look at
    visitedNodes.add(startingNode+1) # startingNode is zero indexed 
    unvisitedNodes.remove(startingNode+1)
    
    while len(unvisitedNodes) is not 0:
        direction = random.randint(0,1)
        newNode = _deterministicNewNode(parents,parentsReversed,parentIndex,walkingIndex,direction)

        if newNode in visitedNodes:
            newNode = _deterministicNewNode(parents,parentsReversed,parentIndex,walkingIndex,1-direction)

        if newNode in visitedNodes:
            # pick a random node if the previous attempts failed
            newNode = random.choice(tuple(unvisitedNodes))

    
        child[walkingIndex] = newNode
        walkingIndex = newNode - 1 # is zero indexed, used to index the parent lists
        visitedNodes.add(newNode)
        unvisitedNodes.remove(newNode)
        parentIndex = 1 - parentIndex # alternate parents
        
    child[walkingIndex] = startingNode + 1
        
    return child