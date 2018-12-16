# any small functions which are used in many places
import numpy as np

def _rangedSet(rangeSize):
	# returns a set thats of 1-indexed values
	# eg if rangeSize is 5 the returned set is {1,2,3,4,5}
	return set (np.linspace(1,rangeSize,rangeSize).astype('int'))

def _reverse(adjList):
	#  returns the adjacency representation of walking through
	# the nodes in the reversed order 
	return np.argsort(adjList)+1

def _startAtOne(array):
	# takes in an array and returns it such that it such that it starts at 1
	indexOne = list(array).index(1)
	oneStarting = np.roll(array, -indexOne)
	return oneStarting