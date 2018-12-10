# implementation of the TSP fitness function
    # phenotype is the adjacency representation of the population
        # as a matrix numpy matrix where rows are individuals
    # distanceMatrix is a matrix containing the distance between nodes

import numpy as np

def _computeFitness(individual, distanceMatrix):
    #keep in mind the correct indexing for the representation
    distances = [distanceMatrix[i,j-1] for (i,j) in enumerate(individual.tolist()[0])]
    
    return sum(distances)

def tsp_fun(phenotype, distanceMatrix):
    fitnessVector = [_computeFitness(individual,distanceMatrix) for individual in phenotype ]
    return np.array(fitnessVector)