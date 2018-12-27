import numpy as np 
import random
from mixins import _startAtOne


def _performCrossover(indexOne, indexTwo, BaseParent, FillParent):
    
    child = [0]*len(BaseParent)
    child[indexOne: indexTwo] = BaseParent[indexOne:indexTwo]

    FillParentFilteredAndReversed = [item for item in FillParent if item not in child][::-1]

    for i in range(len(child)):
        if child[i] == 0:
            child[i] = FillParentFilteredAndReversed.pop()

    return child

def tsp_crossoverByOrder(parents):
    # works on path representation
    # will return 2 children which both have the primary crossover in the same spot

    # determine where to cut
    NVAR = len(parents[0])
    cutLength = random.randint(1,NVAR-1)
    firstSnip = random.randint(0, NVAR-cutLength)
    secondSnip = firstSnip + cutLength

    childOne = _performCrossover(firstSnip, secondSnip,parents[0],parents[1] )
    childTwo = _performCrossover(firstSnip, secondSnip,parents[1],parents[0] )

    return [_startAtOne(childOne), _startAtOne(childTwo)]