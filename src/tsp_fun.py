# implementation of the TSP fitness function
	# phenotype is the adjacency representation of the population
		# as a matrix numpy matrix where rows are individuals
	# distanceMatrix is a matrix containing the distance between nodes

import numpy as np

def _computeFitnessAdjacencyRepresentation(individual, distanceMatrix):
	#keep in mind the correct indexing for the representation
	distances = [distanceMatrix[i,j-1] for (i,j) in enumerate(individual.tolist()[0])]
	return sum(distances)

def _computeFitnessPathRepresentation(individual, distanceMatrix):
	accumulator = 0
	for i in range(len(individual)-1):
		accumulator += distanceMatrix[individual[i]-1, individual[i+1]-1]
	accumulator += distanceMatrix[individual[-1]-1,individual[0]-1]
	
	return accumulator

def tsp_fun(representation,phenotype, distanceMatrix):

	if representation == 'REP_PATH':
		fitnessVector = [_computeFitnessPathRepresentation(individual,distanceMatrix) for individual in phenotype ]
	elif representation == 'REP_ADJACENCY':
		fitnessVector = [_computeFitnessAdjacencyRepresentation(individual,distanceMatrix) for individual in phenotype ]

	return np.array(fitnessVector)