import numpy as np
from tsp_mutationMethods import mapping

# This function takes a matrix OldChrom containing the 
# representation of the individuals in the current population,
# mutates the individuals and returns the resulting population.


def tsp_mutate(REPRESENTATION, MUT_F, OldChrom, MutProb):

	rows, cols = OldChrom.shape
	NewChrom = []

	for row in OldChrom:
		if np.random.random()<MutProb:
			NewRow = MUT_F(row.getA1(), REPRESENTATION)
		else:
			NewRow = row.getA1()
		NewChrom.append(NewRow)

	return np.matrix(NewChrom)