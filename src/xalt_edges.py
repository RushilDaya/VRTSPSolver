import random 

def xalt_edges(oldChromosome, crossoverProbability=1.0):
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
            newChild1 = cross_alternate_edges([oldChromosomeList[i],oldChromosomeList[i+1]])
            newChild2 = cross_alternate_edges([oldChromosomeList[i+1],oldChromosomeList[i]])
        else:
            newChild1 = oldChromosomeList[i]
            newChild2 = oldChromosomeList[i+1]
            
        newChromosomeList.append(newChild1)
        newChromosomeList.append(newChild2)
    
    if len(oldChromosomeList) % 2 !=0:
        newChromosomeList.append(oldChromosomeList[-1])
    
    return np.matrix(newChromosomeList)