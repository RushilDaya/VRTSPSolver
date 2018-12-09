import numpy as np
def inputData(path):
	with open(path) as f:
		content = [(float(x.strip().split()[0]),float(x.strip().split()[1])) for x in f.readlines()]

	x = np.array([x[0] for x in content])
	y = np.array([x[1] for x in content])
	maxVal = max(np.concatenate((x,y)))
	x = x/maxVal
	y = y/maxVal
return x,y
#NVAR=len(x)
