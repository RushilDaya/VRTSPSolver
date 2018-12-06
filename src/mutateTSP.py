import numpy as np

# This function takes a matrix OldChrom containing the 
# representation of the individuals in the current population,
# mutates the individuals and returns the resulting population.


def mutateTSP(MUT_F, OldChrom, MutOpt, REP='adjacency'):
	#Rep indicates the type of representation scheme
	# either adjacency or path

	rows, cols = OldChrom.shape
	NewChrom = np.copy(OldChrom)

	for rIdx in range(0,rows):
		if np.random.random_sample()<MutOpt:
			NewChrom[rIdx] = MUT_F(OldChrom[rIdx].getA1(),REP)

return NewChrom