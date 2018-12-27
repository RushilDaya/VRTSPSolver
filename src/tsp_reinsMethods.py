import numpy as np 
import random

ROUND_ROBIN_SIZE = 10

def _getRoundRobinSize():
    return ROUND_ROBIN_SIZE

def mapping():
	function_mappings = {'tsp_genitor': tsp_genitor,'tsp_randomReplacement': tsp_randomReplacement,
                         'tsp_roundRobin':tsp_roundRobin,'tsp_simpleMuCommaAlpha': tsp_simpleMuCommaAlpha,
                         'tsp_simpleMuPlusAlpha':tsp_simpleMuPlusAlpha}
	return function_mappings

def tsp_genitor(parents,offspring, parentFitness, offspringFitness, elitePercentage=0.0):
    # the genitor algorithm simply replaces the worst N parents with the best N offspring
    # this is effectively a proportional form of elitism as the best members are never lost
    # as long as complete replacement is not selected
    # BUT is not true elitism

    # elite percentage defines the minimum fraction of the parent population to be preserved
    nParents,tmp = parents.shape
    nOffspring,tmp = offspring.shape 
    nElite = int(np.ceil(elitePercentage*nParents))

    nToReplace = nParents - nElite  # preserve nElite numbers and replace nToReplace children
    if nToReplace > nOffspring:
        # if there are fewer offspring than 
        raise Warning('number of offspring too small for specified elitism percentage')
        nToReplace = nOffspring 

    worstParentIndices = np.argsort(-parentFitness)[0:nToReplace]
    bestOffspringIndices = np.argsort(offspringFitness)[0:nToReplace]

    newChrom = parents[:]
    newChrom[worstParentIndices] = offspring[bestOffspringIndices]

    newObjV = parentFitness[:]
    newObjV[worstParentIndices] = offspringFitness[bestOffspringIndices]

    return newChrom.tolist(), newObjV.tolist()

def tsp_randomReplacement(parents,offspring, parentFitness, offspringFitness, elitePercentage=0.0):
    # randomly replace N members of the parents with N members of the offspring
    # doesnt consider elitism

    # elite percentage defines the minimum fraction of the parent population to be preserved
    nParents,tmp = parents.shape
    nOffspring,tmp = offspring.shape 

    nToReplace = nParents

    if nToReplace > nOffspring:
        # if there are fewer offspring than parents randomly insert all the offspring into the population
        raise Warning('poplation is larger than number of offspring')
        nToReplace = nOffspring 

    randomParentIndices = np.argsort(np.array([ random.random() for item in range(nParents)]))[0:nToReplace]
    randomOffspringIndices = np.argsort(np.array([ random.random() for item in range(nOffspring) ]))[0:nToReplace]

    newChrom = parents[:]
    newChrom[randomParentIndices] = offspring[randomOffspringIndices]

    newObjV = parentFitness[:]
    newObjV[randomParentIndices] = offspringFitness[randomOffspringIndices]

    return newChrom.tolist(), newObjV.tolist()

def _randomIndices(num, numRange): # a random set of indices
    return random.sample(range(numRange),num)


def _tallyWinner(item, competitors):
    tally = [1 for competitor in competitors if item < competitor ] # if smaller than the item is more fit
    return sum(tally)


def tsp_roundRobin(parents,offspring,parentFitness,offspringFitness,elitePercentage=0.0):
    # elite percentage doesn't factor in here

    # princple of selection is as follows:
    # combine parents and offspring
    # compare each member to ~10 other random members
    # record how many that member was better than
    # extract the N members with the best win percentages 

    (nParents,tmp) = parents.shape
    (nOffspring,tmp) = offspring.shape

    combinedFitness = parentFitness.tolist()+offspringFitness.tolist()
    combinedFitness = np.array(combinedFitness)
    numCompetitions = _getRoundRobinSize()
    resultsVector = [_tallyWinner(combinedFitness[i], combinedFitness[_randomIndices(numCompetitions,len(combinedFitness))] ) for i in range(len(combinedFitness))]
    rankings = np.argsort(-np.array(resultsVector))[0:nParents]
    indexParents = [i for i in rankings if i < nParents]
    indexOffspring = [i - nParents for i in rankings if i >= nParents ] 
    newChrom = parents[indexParents].tolist() +  offspring[indexOffspring].tolist()
    newObjV = parentFitness[indexParents].tolist() +  offspringFitness[indexOffspring].tolist()

    return newChrom, newObjV

def tsp_simpleMuPlusAlpha(parents,offspring,parentFitness,offspringFitness,elitePercentage=0.0):
    # combines the parents and the offspring
    # take the best N from combination
    # always preserves elites
    nParents,tmp = parents.shape

    combinedFitness = parentFitness.tolist() + offspringFitness.tolist()
    combinedFitness = np.array(combinedFitness)
    ranking = np.argsort(combinedFitness)[0:nParents]

    indexParents = [i for i in ranking if i < nParents]
    indexOffspring = [i - nParents for i in ranking if i >= nParents ] 

    newChrom = parents[indexParents].tolist() +  offspring[indexOffspring].tolist()
    newObjV = parentFitness[indexParents].tolist() +  offspringFitness[indexOffspring].tolist()

    return newChrom, newObjV



def tsp_simpleMuCommaAlpha(parents,offspring,parentFitness,offspringFitness,elitePercentage=0.0):
    # consider only the children take the best N
    # this is the similar to genitor with no elitism i think
    nParents,tmp = parents.shape
    nOffspring,tmp = offspring.shape 

    if nParents > nOffspring:
        raise AttributeError('Offspring population must be larger than parent population')

    ranking = np.argsort(offspringFitness)[0:nParents] # only consider the N best ones

    newChrom = offspring[ranking].tolist()
    newObjV =  offspringFitness[ranking].tolist()

    return newChrom, newObjV    

