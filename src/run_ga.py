import sus
import random
import path2adj
import numpy as np


def run_ga(x, y, NIND, MAXGEN, NVAR, ELITIST, STOP_PERCENTAGE, PR_CROSS, PR_MUT, CROSSOVER, LOCALLOOP, ah1, ah2, ah3):


	GGAP = (1 - ELITIST)
	mean_fits = np.zeros((1,MAXGEN+1))
	worst = np.zeros((1,MAXGEN+1))
	Dist = np.zeros((NVAR,NVAR))
	for i in range(len(x)):
		for j in range(len(y)):
			Dist[i,j] = sqrt((x[i]-x[j])^2+(y[i]-y[j])^2);
	# initialize population
	Chrom = zeros((NIND,NVAR))
	popList = list(range(NVAR))
	for row in range(NIND):
		tmp = popList[:]
		random.shuffle(tmp)
		Chrom[row] = path2adj.path2adj(tmp[:])
		#Chrom[row]=random.shuffle(popList)
	gen = 0
	# number of individuals of equal fitness needed to stop
	stopN = np.ceil(STOP_PERCENTAGE*NIND)
	# evaluate initial population
	ObjV = tspfun(Chrom,Dist)
	best = np.zeros(MAXGEN)
	# generational loop
	while (gen<(MAXGEN-1)):
		sObjV = np.sort(ObjV)
		best[gen] = np.min(ObjV)
		minimum = best[gen]
		mean_fits[gen] = np.mean(ObjV)
		worst[gen] = np.max[ObjV]
		if minimum in ObjV:
			break
		# for t in range(len(ObjV)):
		# 	if (ObjV[t]==minimum):
		# 		break
	            
		#visualizeTSP(x,y,adj2path(Chrom(t,:)), minimum, ah1, gen, best, mean_fits, worst, ah2, ObjV, NIND, ah3);

		if (sObjV[stopN]-sObjV[1] <= 1e-15)
			break

		#assign fitness values to entire population
		FitnV = ranking(ObjV)
		#select individuals for breeding
		SelCh = select(sus.sus, Chrom, FitnV, GGAP)
		#recombine individuals (crossover)
		SelCh = recombin(CROSSOVER,SelCh,PR_CROSS)
		SelCh = mutateTSP(inversion.inversion,SelCh,PR_MUT)
		#evaluate offspring, call objective function
		ObjVSel = tspfun(SelCh,Dist)
		#reinsert offspring into population
		Chrom,ObjV = reins(Chrom,SelCh,1,1,ObjV,ObjVSel)
	            
		Chrom = tsp_ImprovePopulation(NIND, NVAR, Chrom, LOCALLOOP, Dist)
		#increment generation counter
		gen+=1
