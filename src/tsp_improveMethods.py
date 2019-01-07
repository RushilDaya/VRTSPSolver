import numpy as np 
import tsp_swapSubpath
from mixins import _startAtOne

# all these methods assume path representation

def mapping():
	function_mappings = {'tsp_none': tsp_none, 'tsp_localLoops': tsp_localLoops, 'tsp_2opt': tsp_2opt, 'tsp_3opt': tsp_3opt}
	return function_mappings


def tsp_none(path, Dist=None):
	# used when heuristic is not wanted
	return path

def _distSum(path, Dist):
	accumulator = 0
	Nind = len(path)
	for i in range(Nind):
		accumulator += Dist[path[np.mod(i,Nind)]-1, path[np.mod(i+1,Nind)]-1]
	return accumulator

def _swap2opt(path, idx1, idx2):
	return (path[:idx1] + path[idx1:idx2][::-1] + path[idx2:])
	
def _swap3opt(path, a, c, e):
	b,d,f = a+1,c+1,e+1
	sol = []
	sol.append(list(path[:a + 1] + path[e:d - 1:-1] + path[c:b - 1:-1] + path[f:]))
	sol.append(list(path[:a + 1] + path[b:c + 1] + path[e:d - 1:-1] + path[f:]))
	sol.append(list(path[:a + 1] + path[c:b - 1:-1] + path[d:e + 1] + path[f:]))
	sol.append(list(path[:a + 1] + path[d:e + 1] + path[c:b - 1:-1] + path[f:]))
	sol.append(list(path[:a + 1] + path[d:e + 1] + path[b:c + 1] + path[f:]))
	sol.append(list(path[:a + 1] + path[e:d - 1:-1] + path[b:c + 1] + path[f:]))
	sol.append(list(path[:a + 1] + path[c:b - 1:-1] + path[e:d - 1:-1] + path[f:]))
	return sol

# This function improves a single tsp path in path representation by removing local loops up to pathlength 3. 
def tsp_localLoops(path, Dist, maxLoop=25):
	ncities = len(path)
	maxlen = min(maxLoop, ncities//2)
	for loopLength in range(1, maxlen):
		for start in range(ncities):
			stop = np.mod((start+loopLength),ncities)
			idx1 = np.mod((start-1),ncities)
			idx2 = np.mod((stop+1),ncities)
			gain = (Dist[path[idx1]-1,path[start]-1] + Dist[path[stop]-1,path[idx2]-1]) - (Dist[path[idx1]-1,path[stop]-1] - Dist[path[start]-1,path[idx2]-1])
			if (gain > 0):
				path = tsp_swapSubpath.tsp_swapSubpath(ncities, path[:], start, loopLength)
	return _startAtOne(path).tolist()

def tsp_2opt(path, Dist):
	bestDist = _distSum(path,Dist)
	initDist = bestDist+1
	while initDist > bestDist:
		initDist = bestDist
		for (idx1,idx2) in _2segments(len(path)):
			newPath = _swap2opt(path,idx1,idx2)
			newDist = _distSum(newPath,Dist)
			if newDist < bestDist:
				bestDist = newDist
				path = newPath
	return _startAtOne(path).tolist()

def tsp_3opt(path, Dist):
	bestDist = _distSum(path,Dist)
	initDist = bestDist+1
	while initDist > bestDist:
		initDist = bestDist
		for (idx1,idx2,idx3) in _3segments(len(path)):
			newPathList = _swap3opt(path,idx1,idx2,idx3)
			for newPath in newPathList:
				newDist = _distSum(newPath,Dist)
				if newDist < bestDist:
					bestDist = newDist
					path = newPath
	return _startAtOne(path).tolist()

def _2segments(N):
	return ((i, j) for i in range(N) for j in range(i+1, N))

def _3segments(N):
	return ((i, j, k) for i in range(N) for j in range(i+1, N) for k in range(j+1, N))