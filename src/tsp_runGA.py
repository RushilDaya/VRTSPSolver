import random
import tsp_path2adj, tsp_stopCriteria, tsp_fun, tsp_ranking, tsp_select, tsp_reins, tsp_selectionMethods, tsp_mutationMethods, tsp_recombin, tsp_mutate, tsp_improvePopulation
import numpy as np


def _initPopulation(REPRESENTATION,NIND, NVAR):
	# returns an initial population in the appropriate representation
	if REPRESENTATION == 'REP_ADJACENCY':
		Chrom = np.matrix(np.zeros((NIND,NVAR),dtype=int))
		popList = list(range(1,NVAR+1))
		for row in range(NIND):
			tmp = popList[:]
			random.shuffle(tmp)
			Chrom[row] = tsp_path2adj.tsp_path2adj(tmp[:])
		return Chrom

	elif REPRESENTATION == 'REP_PATH':
		Chrom = np.matrix(np.zeros((NIND,NVAR), dtype=int))
		popList = list(range(2,NVAR+1))  # start all path representations at node 1 for consistency
		for row in range(NIND):
			tmp = popList[:]
			random.shuffle(tmp)
			tmp = [1] + tmp 
			Chrom[row] = tmp[:]
		return Chrom

	raise AttributeError('Unknown REPRESENTATION provided')


def tsp_runGA(REPRESENTATION,x, y, NIND, MAXGEN, NVAR, ELITIST, STOP_PERCENTAGE, PR_CROSS, PR_MUT, CROSSOVER, MUTATION, SELECTION,STOPCRITERIA, LOCALLOOP):

	runData = {}
	GGAP = (1 - ELITIST)
	mean_fits = np.zeros(MAXGEN)
	worst = np.zeros(MAXGEN)
	Dist = np.matrix(np.zeros((NVAR,NVAR)))
	for i in range(len(x)):
		for j in range(len(y)):
			Dist[i,j] = np.sqrt((x[i]-x[j])**2+(y[i]-y[j])**2)

	# initialize population
	Chrom = _initPopulation(REPRESENTATION, NIND, NVAR)
	runData['INITIAL_CHROMOSOME']=Chrom
	# number of individuals of equal fitness needed to stop
	stopN = int(np.ceil(STOP_PERCENTAGE*NIND))-1
	# evaluate initial population
	ObjV = tsp_fun.tsp_fun(REPRESENTATION, Chrom,Dist)
	best = np.zeros(MAXGEN)
	

	# generational loop
	runData['GENERATIONAL_DATA'] = {}
	runData['BREAK'] = MAXGEN
	for gen in range(MAXGEN):
		sObjV = np.sort(ObjV)
		best[gen] = np.min(ObjV)
		minimum = best[gen]
		mean_fits[gen] = np.mean(ObjV)
		worst[gen] = np.max(ObjV)
		
		scDepth = 150
		scArgs = [best[:(gen+1)],scDepth,(sObjV/np.max(sObjV)) ,stopN]
		stopCriteria = STOPCRITERIA(scArgs)

		if (stopCriteria):
			runData['BREAK'] = gen
			break

		runData['GENERATIONAL_DATA'][gen]={}
		runData['GENERATIONAL_DATA'][gen]['CHROMOSOME'] = Chrom

		#assign fitness values to entire population
		FitnV = tsp_ranking.tsp_ranking(ObjV) 
		runData['GENERATIONAL_DATA'][gen]['FITNESS'] = ObjV

		#select individuals for breeding
		SelCh = tsp_select.tsp_select(SELECTION, Chrom, FitnV, GGAP)
		#recombine individuals (crossover)
		SelCh = tsp_recombin.tsp_recombin(REPRESENTATION,CROSSOVER,SelCh,PR_CROSS,DISTANCE_MATRIX=Dist) # Dist is used by some crossover methods( Heuristics)
		SelCh = tsp_mutate.tsp_mutate(REPRESENTATION,MUTATION,SelCh,PR_MUT)
		#evaluate offspring, call objective function
		ObjVSel = tsp_fun.tsp_fun(REPRESENTATION,SelCh,Dist)
		#reinsert offspring into population
		Chrom,ObjV = tsp_reins.tsp_reins(Chrom,SelCh,1,[1],ObjV,ObjVSel)


		# Chrom = tsp_ImprovePopulation.tsp_ImprovePopulation(NIND, NVAR, Chrom, LOCALLOOP, Dist)


	runData['RESULTS'] = {
		'BEST':best,
		'WORST':worst,
		'MEAN':mean_fits
	}
	return runData