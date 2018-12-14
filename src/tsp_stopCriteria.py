import numpy as np

THRESHOLD = float('Inf')
#THRESHOLD = (10 ** -5)

def mapping():
	function_mappings = {'runingMean': generic_runingMean,'kImprovement': generic_kImprovement,'bestWorst': generic_bestWorst,'stdDev': generic_stdDev,'phi': generic_phi,'dummy': dummy}
	return function_mappings

def setThreshold(sThreshold):
	global THRESHOLD
	THRESHOLD = sThreshold

def getThreshold():
	return THRESHOLD

## Fully Convergence
#def kIterations(MAX_ITERATIONS,N):
#	return MAX_ITERATIONS<N

def generic_runingMean(scArgs):
	bestList,depth,sObjV,stopN = scArgs
	return runingMean(bestList, depth)

def runingMean(bestList, depth):
	res = (len(bestList)<depth) and float('Inf') or abs(bestList[-depth:][-1]-np.mean(bestList[-depth:]))
	return res<THRESHOLD


def generic_kImprovement(scArgs):
	bestList,depth,sObjV,stopN = scArgs
	return kImprovement(bestList, depth)

def kImprovement(bestList, depth):
	res = (len(bestList)<depth) and float('Inf') or all(bestList[-depth:][i] >= bestList[-depth:][i+1] for i in range(len(bestList[-depth:])-1))
	return res<THRESHOLD

## Partial Convergence
def generic_bestWorst(scArgs):
	bestList,depth,sObjV,stopN = scArgs
	return bestWorst(sObjV, stopN)

def bestWorst(sObjV, stopN):
	res =  (stopN > len(sObjV)) and float('Inf') or abs(sObjV[0]-sObjV[stopN])
	return res<THRESHOLD


def generic_stdDev(scArgs):
	bestList,depth,sObjV,stopN = scArgs
	return stdDev(sObjV)

def stdDev(sObjV):
	res = np.std(sObjV)
	return res<THRESHOLD


def generic_phi(scArgs):
	bestList,depth,sObjV,stopN = scArgs
	return phi(sObjV)

def phi(sObjV):
	res = sObjV[0]/np.mean(sObjV)
	return res<THRESHOLD

def dummy(Dummy):
	return False
