import numpy as np

#THRESHOLD = float('Inf')
THRESHOLD = 0#(10 ** -5)

def mapping():
	function_mappings = {'tsp_runingMean': tsp_generic_runingMean,'tsp_bestWorst': tsp_generic_bestWorst,'tsp_stdDev': tsp_generic_stdDev,'tsp_phi': tsp_generic_phi,'tsp_none': tsp_none}
	return function_mappings

def setThreshold(sThreshold):
	global THRESHOLD
	THRESHOLD = sThreshold

def getThreshold():
	return THRESHOLD

## Fully Convergence
#def kIterations(MAX_ITERATIONS,N):
#	return MAX_ITERATIONS<N

def tsp_generic_runingMean(scArgs):
	bestList,depth,sObjV,stopN = scArgs
	return tsp_runingMean(bestList, depth)

def tsp_runingMean(bestList, depth):
	res = float('Inf')
	if not(len(bestList)<depth):
		res = abs(bestList[-depth:][-1]-np.mean(bestList[-depth:]))
	return res<=THRESHOLD

## Partial Convergence
def tsp_generic_bestWorst(scArgs):
	bestList,depth,sObjV,stopN = scArgs
	return tsp_bestWorst(sObjV, stopN)

def tsp_bestWorst(sObjV, stopN):
	res = float('Inf') 
	if not((stopN > len(sObjV))):
		res = abs(sObjV[0]-sObjV[stopN])
	return res<=THRESHOLD


def tsp_generic_stdDev(scArgs):
	bestList,depth,sObjV,stopN = scArgs
	return tsp_stdDev(sObjV)

def tsp_stdDev(sObjV):
	res = np.std(sObjV)
	return res<=THRESHOLD


def tsp_generic_phi(scArgs):
	bestList,depth,sObjV,stopN = scArgs
	return tsp_phi(sObjV)

def tsp_phi(sObjV):
	res = sObjV[0]/np.mean(sObjV)
	return ((1-res)<=THRESHOLD)

def tsp_none(Dummy):
	return False
