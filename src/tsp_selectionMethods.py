import numpy as np
import math, random

def mapping(REP):
	if(REP=='REP_ADJACENCY' or REP=='REP_PATH'):
		function_mappings = {'tsp_sus': tsp_fps,'tsp_fps': tsp_deterministic_tournament,'tsp_deterministic_tournament': tsp_deterministic_tournament,'tsp_nondeterministic_tournament': tsp_nondeterministic_tournament,'tsp_nondeterministic_tournament_battle': tsp_nondeterministic_tournament_battle,'tsp_rankLinear': tsp_rankLinear,'tsp_rankExponential': tsp_rankExponential,}
		return function_mappings
	else:
		return None

def _getTrailIndex(TrailVal, FitnessSpan):
	return len([ True for item in FitnessSpan if item < TrailVal ])

## PROPORTIONAL (FITNESS) SELECTION BASE
# Stochastic Universal Selection
def tsp_sus(FitnV, Nsel):
	# perform stochastic universal sampling
	Nind = len(FitnV)
	cumfit =  np.cumsum(FitnV)
	stride = cumfit[-1]/Nsel
	randV = random.random()*stride
	trails = np.linspace(0, stride*(Nsel-1), num=Nsel) + randV
	selectedIndices = [_getTrailIndex(item, cumfit) for item in trails]
	#np.random.shuffle(selectedIndices) # in-place function
	return np.array(selectedIndices)

# Fitness Proportionate Selection
def tsp_fps(FitnV, Nsel):
	# perform Fitness Proportionate Selection (Roulette Wheel Selection) sampling
	Nind = len(FitnV)
	cumfit =  np.cumsum(FitnV)
	cumfit /= np.max(cumfit)
	trails = [random.random() for i in range(Nsel)]
	selectedIdx = [_getTrailIndex(item, cumfit) for item in trails]
	np.random.shuffle(selectedIdx) # in-place function
	return np.array(selectedIdx)

# Deterministic Selection
def tsp_deterministic_tournament(FitnV, Nsel):
	# perform deterministic sampling (select Nsel best individuals)
	selectedIdx = np.argsort(FitnV)[:Nsel]
	np.random.shuffle(selectedIdx) # in-place function
	return np.array(selectedIdx)

# Nondeterministic Selection
# params: prob is the probability of been selected.
def tsp_nondeterministic_tournament(FitnV, Nsel, Prob = 0.9):
	# perform non-deterministic sampling
	# Nsel best individuals selected with prob Prob o/w random from rest of the population
	Nind = len(FitnV)
	selectedIdx = np.argsort(FitnV)[:Nsel]
	selectedIdx = [(random.random() < Prob) and elm or FitnV[random.randrange(Nind)] for elm in selectedIdx]
	np.random.shuffle(selectedIdx) # in-place function
	return np.array(selectedIdx)

# Battle Selection
def _compute_battle(x1, x2, FitnV):
	prob = _battleProb(FitnV[x1],FitnV[x2])
	return (prob > random.random()) and x1 or x2

# params: Temp is the teperature of selection state, it act as a pression
def _battleProb(x1, x2, Temp = 1):
	battleProb = (1 + math.exp((x2-x1)/Temp))**(-1)
	return battleProb

def _pairwise(iterable):
    "s -> (s0, s1), (s2, s3), (s4, s5), ..."
    a = iter(iterable)
    return zip(a,a)

# params: battlePop is the percentage of the population selected randomly to create the battle population each time
def tsp_nondeterministic_tournament_battle(FitnV, Nsel, battlePop = 0.1):
	# perform non-deterministic battle tournament sampling 
	# Nsel best individuals selected with prob in fuction of the fitnness of the two selected individuals
	# this method tend to select repetitions of the bests individuals		
	Nind = len(FitnV)
	tournSize = 2**math.floor(math.log(Nind * battlePop, 2))
	#np2 = math.floor(math.log(len(FitnV),2))
	#tournFitnVIdx = np.argsort(FitnV)[:2**np2]
	selectedIdx = []
	for i in range(Nsel):
		tournFitnVIdx = random.sample(range(Nind),tournSize)
		np.random.shuffle(tournFitnVIdx) # in-place function
		while len(tournFitnVIdx)>1:
			tournFitnVIdx = [_compute_battle(x,y,FitnV) for x,y in _pairwise(tournFitnVIdx)]
		selectedIdx.append(tournFitnVIdx[0])
	np.random.shuffle(selectedIdx) # in-place function
	return np.array(selectedIdx)

## RANK SELECTION BASE
def tsp_rankLinear(FitnV, Nsel):
	# perform linear rank based sampling 
	return _tsp_rank(FitnV, Nsel, _linearCalc)

def tsp_rankExponential(FitnV, Nsel):
	# perform exponential rank based sampling 
	return _tsp_rank(FitnV, Nsel, _expCalc)

def _expCalc(idx, *args):
	return (1-math.exp(-idx))

def _linearCalc(idx, selectPress, Nind):
	return (((2-selectPress)/Nind)+((2*idx*(selectPress-1)/(Nind*(Nind-1)))))

# params: selectPress is the selection pression at the actual point, it is act as a temperature
def _tsp_rank(FitnV, Nsel, RANKFUNC, selectPress = 2):
	Nind = len(FitnV)
	sortedIdx = np.argsort(-FitnV)
	selectProb = [RANKFUNC(idx, selectPress, Nind) for idx in range(Nind)]
	selectProb /= np.cumsum(selectProb)[-1] #Normalization
	cumfit = np.cumsum(selectProb)
	trails = [random.random() for i in range(Nsel)]
	selectedProbIdx = [_getTrailIndex(item, cumfit) for item in trails]
	selectedIdx = [sortedIdx[idx] for idx in selectedProbIdx]
	np.random.shuffle(selectedIdx) # in-place function
	return np.array(selectedIdx)

