import numpy as np 

 REINS_F( runParents, runOffSpring, elitePercentage)

def genitor(parents,offspring, parentFitness, offspringFitness, elitePercentage=0.0):
    # the genitor algorithm simply replaces the worst N parents with the best N offspring
    # this is effectively a proportional form of elitism as the best members are never lost
    # as long as complete replacement is not selected
    # BUT is not true elitism

    # elite percentage defines the minimum fraction of the parent population to be preserved
    nParents, = parents.shape
    nOffspring, = offspring.shape 
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

def randomReplacement(Parents,Offspring, parentFitness, offspringFitness, elitePercentage=0.0):
    # randomly replace N members of the parents with N members of the offspring
    # doesnt consider elitism

    # elite percentage defines the minimum fraction of the parent population to be preserved
    nParents, = parents.shape
    nOffspring, = offspring.shape 

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