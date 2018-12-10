import sus, inversion
import random
import path2adj, tspfun, ranking, tspSelect, reins, tspfun, recombin, mutateTSP, tsp_ImprovePopulation
import numpy as np

def run_ga(x, y, NIND, MAXGEN, NVAR, ELITIST, STOP_PERCENTAGE, PR_CROSS, PR_MUT, CROSSOVER, LOCALLOOP):

	runData = {
				'PARAMETERS':{
					'NIND':NIND,
					'MAXGEN':MAXGEN,
					'NVAR':NVAR,
					'ELITIST':ELITIST,
					'STOP_PERCENTAGE':STOP_PERCENTAGE,
					'PR_CROSS':PR_CROSS,
					'PR_MUT':PR_MUT,
					'LOCALLOOP':LOCALLOOP
			  	}			
			  }
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
	runData['INITIAL_CHROMOSOME']=Chrom
	gen = 0
	# number of individuals of equal fitness needed to stop
	stopN = int(np.ceil(STOP_PERCENTAGE*NIND))-1
	# evaluate initial population
	ObjV = tspfun.tspfun(Chrom,Dist)
	best = np.zeros(MAXGEN)
	# generational loop
	runData['GENERATIONAL_DATA'] = {}
	while (gen<(MAXGEN-1)):
		runData['GENERATIONAL_DATA'][gen]={}
		sObjV = np.sort(ObjV)
		best[gen] = np.min(ObjV)
		minimum = best[gen]
		mean_fits[gen] = np.mean(ObjV)
		worst[gen] = np.max(ObjV)
	            
		#visualizeTSP(x,y,adj2path(Chrom(t,:)), minimum, ah1, gen, best, mean_fits, worst, ah2, ObjV, NIND, ah3);

		if ((sObjV[stopN]-sObjV[0]) <= (10 ** -5)):
			break
		runData['GENERATIONAL_DATA'][gen]['START_GENERATION_CHROMOSOMES'] = Chrom
		#assign fitness values to entire population
		FitnV = ranking.ranking(ObjV)
		runData['GENERATIONAL_DATA'][gen]['STARTING_FITNESS'] = ObjV
		#select individuals for breeding
		SelCh = tspSelect.tspSelect(sus.sus, Chrom, FitnV, GGAP)
		runData['GENERATIONAL_DATA'][gen]['SELECTED_CHROMOSOMES'] = SelCh
		#recombine individuals (crossover)
		SelCh = recombin.recombin(CROSSOVER,SelCh,PR_CROSS)
		runData['GENERATIONAL_DATA'][gen]['RECOMBINED_CHROMOSOMES'] = SelCh
		SelCh = mutateTSP.mutateTSP(inversion.inversion,SelCh,PR_MUT)
		runData['GENERATIONAL_DATA'][gen]['MUTATED_CHROMOSOMES'] = SelCh
		#evaluate offspring, call objective function
		ObjVSel = tspfun.tspfun(SelCh,Dist)
		#reinsert offspring into population
		Chrom,ObjV = reins.reins(Chrom,SelCh,1,[1],ObjV,ObjVSel)
		runData['GENERATIONAL_DATA'][gen]['REINSERTED_CHROMOSOMES'] = Chrom
	            
	#	Chrom = tsp_ImprovePopulation.tsp_ImprovePopulation(NIND, NVAR, Chrom, LOCALLOOP, Dist)
	#	logger.info('RUN=%d|GENERATION=%d|END_GENERATION_CHROMOSOMES=%s',RUN_NUMBER,gen,Chrom)
		#increment generation counter
		gen+=1

	runData['RESULTS'] = {
		'BEST':best,
		'WORST':worst,
		'MEAN':mean_fits
	}
	return runData