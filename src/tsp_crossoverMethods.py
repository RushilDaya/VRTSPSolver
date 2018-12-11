import random 
import numpy as np
import tsp_crossAlternateEdges

def mapping(REP):
	if(REP=='REP_ADJACENCY'):
		function_mappings = {'tsp_xaltEdges': tsp_xaltEdges,}
		return function_mappings
	else:
		return None



def tsp_xaltEdges(oldChromosome, crossoverProbability=1.0):
	# oldChromosome is a matrix 
	# crossoverProbability is a float scalar in range [0,1]
	# returns a new chromosome matrix
	
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