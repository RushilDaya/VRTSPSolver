import numpy as np
import tsp_exceptions

# REINS.M        (RE-INSertion of offspring in population replacing parents)
# This function reinserts offspring in the population.



def tsp_reins(REINS_F, parentChrom, offspringChrom,fitnessParents,fitnessChildren,elitePercentage,SUBPOP=1):

	(nindParent,tmp) = parentChrom.shape
	(nindOffspring,tmp) = offspringChrom.shape 

	if len(fitnessParents) != nindParent or len(fitnessChildren) !- nindOffspring:
		raise tsp_exceptions.disagree('Dimension mismatch between chromosomes and fitness vectors')

	if nindParent % SUBPOP != 0 or nindOffspring % SUBPOP != 0:
		raise tsp_exceptions.disagree('Cannot equally sized subpopulations')
	
	nParents = nindParent//SUBPOP
	nOffspring = nindOffspring//SUBPOP

	newChrom = []
	objVCh = []
	for irun in range(SUBPOP):
		runParents = parentChrom[nParents*irun:nParents*(irun+1)]
		runParentFitness = fitnessParents[nParents*irun:nParents*(irun+1)]
		runOffSpring = runOffSpring[nOffspring*irun:nOffspring*(irun+1)]
		runOffSpringFitness = fitnessChildren[nOffspring*irun:nOffspring*(irun+1)]

		newChromSub, objVSub = REINS_F( runParents, runOffSpring, runParentFitness, runOffSpringFitness, elitePercentage)
		newChrom = newChrom + newChromSub
		objVCh = objVCh + objVSub
	
	return np.matrix(newChrom), np.array(objVCh)

