import random
import tsp_path2adj, tsp_fun, tsp_ranking, tsp_select, tsp_reins, tsp_selectionMethods, tsp_mutationMethods, tsp_recombin, tsp_mutate, tsp_improvePopulation
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
	else
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


def tsp_runGA(REPRESENTATION,x, y, NIND, MAXGEN, NVAR, ELITIST, STOP_PERCENTAGE, PR_CROSS, PR_MUT, CROSSOVER, MUTATION, SELECTION, LOCALLOOP):

	runData = {}
	GGAP = (1 - ELITIST)
	mean_fits = np.zeros(MAXGEN)
	worst = np.zeros(MAXGEN)
	Dist = _distInit(x,y,NVAR)
	# initialize population
	Chrom = _initPopulation(REPRESENTATION, NIND, NVAR)
	Chrom[-1] = _minimalInitialPath(Dist, REPRESENTATION)
	runData['INITIAL_CHROMOSOME']=Chrom
	# number of individuals of equal fitness needed to stop
	#stopN = int(np.ceil(STOP_PERCENTAGE*NIND))-1
	# evaluate initial population
	ObjV = tsp_fun.tsp_fun(REPRESENTATION, Chrom, Dist)
	best = np.zeros(MAXGEN)
	# generational loop
	#runData['GENERATIONAL_DATA'] = {}
	for gen in range(MAXGEN):
		#runData['GENERATIONAL_DATA'][gen]={}
		sObjV = np.sort(ObjV)
		best[gen] = np.min(ObjV)
		minimum = best[gen]
		mean_fits[gen] = np.mean(ObjV)
		worst[gen] = np.max(ObjV)
		
		#visualizeTSP(x,y,adj2path(Chrom(t,:)), minimum, ah1, gen, best, mean_fits, worst, ah2, ObjV, NIND, ah3);

		# STOP CRITERIA
		#if ((sObjV[stopN]-sObjV[0]) <= (10 ** -5)):
			#break

		#runData['GENERATIONAL_DATA'][gen]['START_GENERATION_CHROMOSOMES'] = Chrom
		#assign fitness values to entire population
		FitnV = tsp_ranking.tsp_ranking(ObjV) 
		#runData['GENERATIONAL_DATA'][gen]['STARTING_FITNESS'] = ObjV
		#select individuals for breeding
		SelCh = tsp_select.tsp_select(SELECTION, Chrom, FitnV, GGAP)
		#runData['GENERATIONAL_DATA'][gen]['SELECTED_CHROMOSOMES'] = SelCh
		#recombine individuals (crossover)
		SelCh = tsp_recombin.tsp_recombin(REPRESENTATION,CROSSOVER,SelCh,PR_CROSS,DISTANCE_MATRIX=Dist) # Dist is used by some crossover methods( Heuristics)
		#runData['GENERATIONAL_DATA'][gen]['RECOMBINED_CHROMOSOMES'] = SelCh
		SelCh = tsp_mutate.tsp_mutate(REPRESENTATION,MUTATION,SelCh,PR_MUT)
		#runData['GENERATIONAL_DATA'][gen]['MUTATED_CHROMOSOMES'] = SelCh
		#evaluate offspring, call objective function
		ObjVSel = tsp_fun.tsp_fun(REPRESENTATION,SelCh,Dist)
		#reinsert offspring into population
		Chrom,ObjV = tsp_reins.tsp_reins(Chrom,SelCh,1,[1],ObjV,ObjVSel)
		#runData['GENERATIONAL_DATA'][gen]['REINSERTED_CHROMOSOMES'] = Chrom
							
		#Chrom = tsp_ImprovePopulation.tsp_ImprovePopulation(NIND, NVAR, Chrom, LOCALLOOP, Dist)

	runData['RESULTS'] = {
		'BEST':best,
		'WORST':worst,
		'MEAN':mean_fits
	}
	return runData