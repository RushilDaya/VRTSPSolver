import numpy as np
from tsp_crossoverMethods import mapping

# This function performs recombination between pairs of individuals
# and returns the new individuals after mating. The function handles
# multiple populations and calls the low-level recombination function
# for the actual recombination process.

def tsp_recombin(REPRESENTATION, REC_F, Chrom, RecOpt = 0.7, SUBPOP = 1, DISTANCE_MATRIX=None):
	
	# make sure the recombination is correct for the representation
	funcName = REC_F.__name__
	validMethods = mapping(REPRESENTATION).keys()
	if funcName not in validMethods:
		raise AttributeError('%s not a valid crossover method for %s',funcName,REPRESENTATION)

	if (RecOpt < 0 or RecOpt > 1):
		raise outOfRange("RecOpt must be a scalar in [0, 1]")
	
	# Identify the population size (Nind)
	Nind, Nvar = Chrom.shape

	if ((Nind/SUBPOP) != np.fix(Nind/SUBPOP)).all():
		raise disagree('Chrom and SUBPOP disagree')
	Nind = Nind//SUBPOP  #Compute number of individuals per subpopulation
	
	# Select individuals of one subpopulation and call low level function
	
	NewChrom = None
	for irun in range(SUBPOP):
		ChromSub = Chrom[(irun)*Nind:(irun+1)*Nind]
		NewChromSub = REC_F(ChromSub, RecOpt, DISTANCE_MATRIX)
		NewChrom = NewChrom and numpy.concatenate((NewChrom, NewChromSub)) or np.copy(NewChromSub)
	
	return np.matrix(NewChrom)