import numpy as np

def mapping():
	function_mappings = {'tsp_runingMean': tsp_runingMean,'tsp_bestWorst': tsp_bestWorst,'tsp_stdDev': tsp_stdDev,'tsp_phi': tsp_phi,'tsp_none': tsp_none}
	return function_mappings

## Fully Convergence
#def kIterations(MAX_ITERATIONS,N):
#	return MAX_ITERATIONS<N

def tsp_genericStopCriteria(scArgs):
	STOPCRITERIA,THRESHOLD,bestList,depth,sObjV,stopN,GEN,MAXGEN = scArgs
	minGen = 50
	if not(GEN < int(minGen)):
		return STOPCRITERIA(THRESHOLD,bestList,depth,sObjV,stopN,GEN)
	else:
		False

def tsp_runingMean(THRESHOLD,bestList,depth,sObjV,stopN,GEN):
	if not(depth>=len(bestList)):
		return (abs(bestList[-depth:][-1]/np.mean(bestList[-depth:]))<=THRESHOLD)
	else:
		return False

## Partial Convergence
def tsp_bestWorst(THRESHOLD,bestList,depth,sObjV,stopN,GEN):
	if not((stopN > len(sObjV))):
		return abs(sObjV[0]-sObjV[stopN])<=THRESHOLD
	else:
		return False

def tsp_stdDev(THRESHOLD,bestList,depth,sObjV,stopN,GEN):
	res = np.std(bestList[-depth:])
	return res<=THRESHOLD

def tsp_phi(THRESHOLD,bestList,depth,sObjV,stopN,GEN):
	res = sObjV[0]/np.mean(sObjV)
	return (1-res<=THRESHOLD)

def tsp_none(*args):
	return False
