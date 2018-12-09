import sus, inversion
import random
import path2adj, tspfun, ranking, tspSelect, reins, tspfun, recombin, mutateTSP, tsp_ImprovePopulation
import numpy as np


def run_ga(x, y, NIND, MAXGEN, NVAR, ELITIST, STOP_PERCENTAGE, PR_CROSS, PR_MUT, CROSSOVER, LOCALLOOP):

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
		Chrom[row] = path2adj.path2adj(tmp[:])
		#Chrom[row]=random.shuffle(popList)
	gen = 0
	# number of individuals of equal fitness needed to stop
	stopN = int(np.ceil(STOP_PERCENTAGE*NIND))-1
	# evaluate initial population
	print(Chrom)
	print(Dist)
	ObjV = tspfun.tspfun(Chrom,Dist)
	best = np.zeros(MAXGEN)
	# generational loop
	while (gen<(MAXGEN-1)):
		print(gen)
		sObjV = np.sort(ObjV)
		best[gen] = np.min(ObjV)
		minimum = best[gen]
		mean_fits[gen] = np.mean(ObjV)
		worst[gen] = np.max(ObjV)
	            
		#visualizeTSP(x,y,adj2path(Chrom(t,:)), minimum, ah1, gen, best, mean_fits, worst, ah2, ObjV, NIND, ah3);

		if ((sObjV[stopN]-sObjV[0]) <= (10 ** -5)):
			break

		#assign fitness values to entire population
		FitnV = ranking.ranking(ObjV)
		#select individuals for breeding
		SelCh = tspSelect.tspSelect(sus.sus, Chrom, FitnV, GGAP)
		#recombine individuals (crossover)
		SelCh = recombin.recombin(CROSSOVER,SelCh,PR_CROSS)
		SelCh = mutateTSP.mutateTSP(inversion.inversion,SelCh,PR_MUT)
		#evaluate offspring, call objective function
		ObjVSel = tspfun.tspfun(SelCh,Dist)
		#reinsert offspring into population
		print(Chrom.shape)
		print(SelCh.shape)
		print(ObjV.shape)
		print(ObjVSel.shape)
		Chrom,ObjV = reins.reins(Chrom,SelCh,1,[1],ObjV,ObjVSel)
	            
		Chrom = tsp_ImprovePopulation.tsp_ImprovePopulation(NIND, NVAR, Chrom, LOCALLOOP, Dist)
		#increment generation counter
		gen+=1

	print(Chrom)
