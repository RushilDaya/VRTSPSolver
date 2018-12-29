import random
import tsp_path2adj, tsp_stopCriteria, tsp_fun, tsp_ranking, tsp_select, tsp_reins, tsp_selectionMethods, tsp_mutationMethods, tsp_recombin, tsp_mutate, tsp_improvePopulation
import numpy as np

def _distInit(x,y,NVAR):
	values = [np.sqrt((x[i]-x[j])**2+(y[i]-y[j])**2) for i in range(len(x)) for j in range(len(y))]
	Dist = np.matrix(values)
	return Dist.reshape((NVAR,NVAR))

def _minimalInitialPath(Dist, REPRESENTATION):
	Nrow, Ncol = Dist.shape
	idx = 0
	path = [0]
	remains = list(range(1,Ncol))
	while remains != []:
		val = float('Inf')
		row = list(Dist[idx].getA1())
		for elm in row:
			idx = row.index(elm)
			if elm != 0 and elm<val and idx not in path:
					val = elm
		idx = row.index(val)
		path.append(idx)
		remains.remove(idx)
	path = np.array(path) + 1
	if REPRESENTATION == 'REP_ADJACENCY':
		path = tsp_path2adj.tsp_path2adj(path[:])
	return path

def _initPopulation(REPRESENTATION, NIND, NVAR):
	# returns an initial population in the appropriate representation
	Chrom = np.matrix(np.zeros((NIND,NVAR), dtype=int))
	
	if REPRESENTATION == 'REP_ADJACENCY':
		popList = list(range(1,NVAR+1))
	elif REPRESENTATION == 'REP_PATH':
		popList = list(range(2,NVAR+1))	# start all path representations at node 1 for consistency
	else:
		raise AttributeError('Unknown REPRESENTATION provided')
	
	for row in range(NIND):
		tmp = popList[:]
		random.shuffle(tmp)
		if REPRESENTATION == 'REP_ADJACENCY':
			Chrom[row] = tsp_path2adj.tsp_path2adj(tmp[:])
		elif REPRESENTATION == 'REP_PATH':
			tmp = [1] + tmp 
			Chrom[row] = tmp[:]
	return Chrom


def tsp_runGA(REPRESENTATION,x, y, NIND, OFFSPRING_FACTOR, MAXGEN, NVAR, ELITE_PERCENTAGE, STOP_PERCENTAGE, PR_CROSS, PR_MUT, CROSSOVER, MUTATION, SELECTION,STOPCRITERIA,REINSERTION ,IMPROVE_POP):
	# ELITE_PERCENTAGE is the fraction of best parents which are always preserved
	# OFFSPRING_FACTOR*NIND is the number of children which need are produced in each generation

	runData = {}
	Dist = _distInit(x,y,NVAR)

	# initialize population
	Chrom = _initPopulation(REPRESENTATION, NIND, NVAR)
	Chrom[-1] = _minimalInitialPath(Dist, REPRESENTATION)
	runData['INITIAL_CHROMOSOME']=Chrom

	# evaluate initial population
	ObjV = tsp_fun.tsp_fun(REPRESENTATION, Chrom, Dist)
	
	# generational loop
	#runData['GENERATIONAL_DATA'] = {}
	best = []#np.zeros(MAXGEN)
	mean_fits = []#np.zeros(MAXGEN)
	worst = []#np.zeros(MAXGEN)
	FitnVList = []
	CromList = []

	# STOP CRITERIA 
	# number of individuals of equal fitness needed to stop
	#stopN = int(np.ceil(STOP_PERCENTAGE*NIND))-1
	
	for gen in range(MAXGEN):
		#runData['GENERATIONAL_DATA'][gen]={}
		if ((gen%1)==0):
			sObjV = np.sort(ObjV)
			minimum = np.min(ObjV)
			best.append(minimum)
			mean_fits.append(np.mean(ObjV))
			worst.append(np.max(ObjV))

		#STOP CRITERIA
		#scDepth = 150
		#scArgs = [best[:(gen+1)],scDepth,(sObjV/np.max(sObjV)) ,stopN]
		#stopCriteria = STOPCRITERIA(scArgs)

		#if (stopCriteria):
		#	runData['BREAK'] = gen
		#	break

		#runData['GENERATIONAL_DATA'][gen]={}

		#assign fitness values to entire population
		#FitnV = tsp_ranking.tsp_ranking(ObjV) 

		#select individuals for breeding
		SelCh = tsp_select.tsp_select(SELECTION, Chrom, ObjV, OFFSPRING_FACTOR)
		#recombine individuals (crossover)
		SelCh = tsp_recombin.tsp_recombin(REPRESENTATION,CROSSOVER,SelCh,PR_CROSS,DISTANCE_MATRIX=Dist) # Dist is used by some crossover methods( Heuristics)
		SelCh = tsp_mutate.tsp_mutate(REPRESENTATION,MUTATION,SelCh,PR_MUT)
		#evaluate offspring, call objective function
		ObjVSel = tsp_fun.tsp_fun(REPRESENTATION,SelCh,Dist)
		#reinsert offspring into population
		Chrom,ObjV = tsp_reins.tsp_reins(REINSERTION, Chrom,SelCh,ObjV,ObjVSel,ELITE_PERCENTAGE)

		Chrom = tsp_improvePopulation.tsp_improvePopulation(REPRESENTATION, IMPROVE_POP, Chrom, Dist)
		ObjV = tsp_fun.tsp_fun(REPRESENTATION,Chrom,Dist)
		#NOTE: the recalculation needs to be done after improvement @victor if you have a more efficient method please change this
		
		if ((gen%20)==0):
			FitnVList.append(ObjV)
			CromList.append(Chrom)

	runData['FINAL_CHROMOSOME']=Chrom
	runData['FINAL_FITNESS']=ObjV
	
	runData['RESULTS'] = {
		'BEST':best,
		'WORST':worst,
		'MEAN':mean_fits
	}
	return runData