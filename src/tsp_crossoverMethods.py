import random 
import numpy as np
import tsp_crossAlternateEdges
import tsp_crossoverByGreedyHeuristic
import tsp_crossoverByProbabilisticHeuristic

def mapping(REP):
	if(REP=='REP_ADJACENCY'):
		function_mappings = {'tsp_xaltEdges': tsp_xaltEdges,'tsp_greedyHeuristicCrossover':tsp_greedyHeuristicCrossover,
							 'tsp_probabilisticHeuristicCrossover':tsp_probabilisticHeuristicCrossover}
		return function_mappings
	else:
		return None

# The functions which come below are equivelent besides the method they call
# should actually just reduce this to a single function

def tsp_xaltEdges(oldChromosome, crossoverProbability=1.0, distanceMatrix=None):
	# only applies to adjacency representation
	# oldChromosome is a matrix 
	# crossoverProbability is a float scalar in range [0,1]
	# returns a new chromosome matrix
	# Dist is not used
	
	oldChromosomeList = oldChromosome.tolist()
	
	rows = len(oldChromosomeList)
	if rows % 2 != 0:
		rows = rows-1
	
	newChromosomeList =  []
	
	for i in range(0,rows,2):
		if random.random() < crossoverProbability:
			newChild1 = tsp_crossAlternateEdges.tsp_crossAlternateEdges([oldChromosomeList[i],oldChromosomeList[i+1]])
			newChild2 = tsp_crossAlternateEdges.tsp_crossAlternateEdges([oldChromosomeList[i+1],oldChromosomeList[i]])
		else:
			newChild1 = oldChromosomeList[i]
			newChild2 = oldChromosomeList[i+1]
			
		newChromosomeList.append(newChild1)
		newChromosomeList.append(newChild2)
	
	if len(oldChromosomeList) % 2 !=0:
		newChromosomeList.append(oldChromosomeList[-1])
	
	return np.matrix(newChromosomeList)

def tsp_greedyHeuristicCrossover(oldChromosome, crossoverProbability=1.0, distanceMatrix=None):
	# only applies to adjacency representation
	# oldChromosome is a matrix
	# crossoverProbability is between 0 and 1

	oldChromosomeList = oldChromosome.tolist()
	
	rows = len(oldChromosomeList)
	if rows % 2 != 0:
		rows = rows-1
	
	newChromosomeList =  []
	
	for i in range(0,rows,2):
		if random.random() < crossoverProbability:
			newChild1 = tsp_crossoverByGreedyHeuristic.tsp_crossoverByGreedyHeuristic([oldChromosomeList[i],oldChromosomeList[i+1]],distanceMatrix)
			newChild2 = tsp_crossoverByGreedyHeuristic.tsp_crossoverByGreedyHeuristic([oldChromosomeList[i+1],oldChromosomeList[i]],distanceMatrix)
		else:
			newChild1 = oldChromosomeList[i]
			newChild2 = oldChromosomeList[i+1]
			
		newChromosomeList.append(newChild1)
		newChromosomeList.append(newChild2)
	
	if len(oldChromosomeList) % 2 !=0:
		newChromosomeList.append(oldChromosomeList[-1])
	
	return np.matrix(newChromosomeList)

def tsp_probabilisticHeuristicCrossover(oldChromosome, crossoverProbability=1.0, distanceMatrix=None):
	# only applies to adjacency representation
	# oldChromosome is a matrix
	# crossoverProbability is between 0 and 1

	oldChromosomeList = oldChromosome.tolist()
	
	rows = len(oldChromosomeList)
	if rows % 2 != 0:
		rows = rows-1
	
	newChromosomeList =  []
	
	for i in range(0,rows,2):
		if random.random() < crossoverProbability:
			newChild1 = tsp_crossoverByProbabilisticHeuristic.tsp_crossoverByProbabilisticHeuristic([oldChromosomeList[i],oldChromosomeList[i+1]],distanceMatrix)
			newChild2 = tsp_crossoverByProbabilisticHeuristic.tsp_crossoverByProbabilisticHeuristic([oldChromosomeList[i+1],oldChromosomeList[i]],distanceMatrix)
		else:
			newChild1 = oldChromosomeList[i]
			newChild2 = oldChromosomeList[i+1]
			
		newChromosomeList.append(newChild1)
		newChromosomeList.append(newChild2)
	
	if len(oldChromosomeList) % 2 !=0:
		newChromosomeList.append(oldChromosomeList[-1])
	
	return np.matrix(newChromosomeList)