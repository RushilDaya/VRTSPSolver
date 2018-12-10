import random
import tsp_path2adj, tsp_fun, tsp_ranking, tsp_select, tsp_reins, tsp_sus, tsp_inversion, tsp_recombin, tsp_mutate, tsp_improvePopulation
import numpy as np


def tsp_runGA(x, y, NIND, MAXGEN, NVAR, ELITIST, STOP_PERCENTAGE, PR_CROSS, PR_MUT, CROSSOVER, LOCALLOOP):

	GGAP = (1 - ELITIST)
	mean_fits = np.zeros(MAXGEN)
	worst = np.zeros(MAXGEN)
	Dist = np.matrix(np.zeros((NVAR,NVAR)))
	for i in range(len(x)):
		for j in range(len(y)):
			Dist[i,j] = np.sqrt((x[i]-x[j])**2+(y[i]-y[j])**2)
	# initialize population
	Chrom = np.matrix(np.zeros((NIND,NVAR),dtype=int))
	popList = list(range(1,NVAR+1))
	for row in range(NIND):
		tmp = popList[:]
		random.shuffle(tmp)
		Chrom[row] = tsp_path2adj.tsp_path2adj(tmp[:])
		#Chrom[row]=random.shuffle(popList)
	gen = 0
	# number of individuals of equal fitness needed to stop
	stopN = int(np.ceil(STOP_PERCENTAGE*NIND))-1
	# evaluate initial population
	ObjV = tsp_fun.tsp_fun(Chrom,Dist)
	best = np.zeros(MAXGEN)
	# generational loop
	while (gen<(MAXGEN-1)):
		sObjV = np.sort(ObjV)
		best[gen] = np.min(ObjV)
		minimum = best[gen]
		mean_fits[gen] = np.mean(ObjV)
		worst[gen] = np.max(ObjV)
	            
		#visualizeTSP(x,y,adj2path(Chrom(t,:)), minimum, ah1, gen, best, mean_fits, worst, ah2, ObjV, NIND, ah3);

		if ((sObjV[stopN]-sObjV[0]) <= (10 ** -5)):
			break

		#assign fitness values to entire population
		FitnV = tsp_ranking.tsp_ranking(ObjV)
		#select individuals for breeding
		SelCh = tsp_select.tsp_select(tsp_sus.tsp_sus, Chrom, FitnV, GGAP)
		#recombine individuals (crossover)
		SelCh = tsp_recombin.tsp_recombin(CROSSOVER,SelCh,PR_CROSS)
		SelCh = tsp_mutate.tsp_mutate(tsp_inversion.tsp_inversion,SelCh,PR_MUT)
		#evaluate offspring, call objective function
		ObjVSel = tsp_fun.tsp_fun(SelCh,Dist)
		#reinsert offspring into population
		Chrom,ObjV = tsp_reins.tsp_reins(Chrom,SelCh,1,[1],ObjV,ObjVSel)
	            
		Chrom = tsp_improvePopulation.tsp_improvePopulation(NIND, NVAR, Chrom, LOCALLOOP, Dist)
		#increment generation counter
		gen+=1