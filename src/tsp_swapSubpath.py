import numpy as np

def tsp_swapSubpath(ncities, path, start, length):

	i = start
	j = np.mod((start + length),ncities)
	#j = np.mod((start-1 + length-1), ncities) + 1
	
	while (length > 0):
		temp = path[i]
		path[i] = path[j]
		path[j] = temp
		length -= 2
		i = np.mod(i+1,ncities)
		j = np.mod(j-1,ncities)

	return path