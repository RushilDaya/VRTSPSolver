# a rank based fitness assignment
import numpy as np
from tsp_exceptions import NotImplementedError

def _linearRankFunction(index, selectionPressure, populationSize):
    return 2- selectionPressure + 2*index*(selectionPressure -1)/(populationSize-1)

def _nonlinearRankFunction(index, selectionPressure,populationSize):
    # a ranking function which makes use of polynomial roots
    # not really sure what its doing
    # its pretty inefficient doing the root calculation here
    # wasting most of our computation
    polynomialCoeffs = np.full(populationSize, selectionPressure)
    polynomialCoeffs[0] = selectionPressure - populationSize
    rootFactor = abs(np.roots(polynomialCoeffs)[0])
    fullArray = [pow(rootFactor,i) for i in  range(populationSize)]
    return fullArray[index]*populationSize/sum(fullArray)
    
    
    
    
def _generateRankingArray(populationSize, selectionPressure, rankingType):

    
    if rankingType.lower() == 'linear':
        if selectionPressure < 1 or selectionPressure > 2:
            raise ValueError('selectionPressure must be in range [1,0]')

        rankValues = [ _linearRankFunction(i,selectionPressure, populationSize) for i in range(populationSize) ] 
        return np.array(rankValues)

    if rankingType.lower() == 'non_linear':
        if selectionPressure < 1 or selectionPressure > 2:
            raise ValueError('selectionPressure must be in range [1,0]')
            
        rankValues = [ _nonlinearRankFunction(i,selectionPressure, populationSize) for i in range(populationSize) ] 
        return np.array(rankValues)
    else:
        raise ValueError('unknown ranking type provided')

def tsp_ranking(fitnessVector, rankingOptions=[2,'linear'], subPopulations=1):
    # fitnessVector is a numpy array of fitness values
    # rankingOptions [x,y] -> x is the selection pressure in range [1:2]
    #                      -> y is the ranking type enum ('linear', 'non_linear')
    #                       if ranking options has length > 2 it is assumed
    # subPopulations defines how many subpopulations the fitnessVector is split when computing the ranking

    if subPopulations != 1:
        raise NotImplementedError('sub populations not yet implemented')

    populationSize = len(fitnessVector)
    rankingArray = _generateRankingArray(populationSize,rankingOptions[0],rankingOptions[1])

    # a sorted the argsort values allows us to get the indices we can use to index ranking array
    sortIndices = np.argsort(np.argsort(-fitnessVector)) # negate to sort in descending order
    rankings = [rankingArray[i] for i in sortIndices]
    return np.array(rankings)