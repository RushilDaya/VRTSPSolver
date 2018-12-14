import random
import tsp_path2adj, tsp_stopCriteria, tsp_fun, tsp_ranking, tsp_select, tsp_reins, tsp_selectionMethods, tsp_mutationMethods, tsp_recombin, tsp_mutate, tsp_improvePopulation
import numpy as np


def tsp_runGA(x, y, NIND, MAXGEN, NVAR, ELITIST, STOP_PERCENTAGE, PR_CROSS, PR_MUT, CROSSOVER, MUTATION, SELECTION, STOPCRITERIA, LOCALLOOP):

	runData = {
				# 'NODES':{
				# 	'X':x,
				# 	'Y':y
				# },
				# 'PARAMETERS':{
				# 	'NIND':NIND,
				# 	'MAXGEN':MAXGEN,
				# 	'NVAR':NVAR,
				# 	'ELITIST':ELITIST,
				# 	'STOP_PERCENTAGE':STOP_PERCENTAGE,
				# 	'PR_CROSS':PR_CROSS,
				# 	'PR_MUT':PR_MUT,
				# 	'LOCALLOOP':LOCALLOOP
			 #  	}			
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
		Chrom[row] = tsp_path2adj.tsp_path2adj(tmp[:])
		#Chrom[row]=random.shuffle(popList)
	runData['INITIAL_CHROMOSOME']=Chrom
	# number of individuals of equal fitness needed to stop
	stopN = int(np.ceil(STOP_PERCENTAGE*NIND))-1
	# evaluate initial population
	ObjV = tsp_fun.tsp_fun(Chrom,Dist)
	best = np.zeros(MAXGEN)
	
	# set Threshold
	tsp_stopCriteria.setThreshold((10**-5))
	# generational loop
	# runData['GENERATIONAL_DATA'] = {}
	# runData['BREAK'] = MAXGEN
	for gen in range(MAXGEN):
	#while (gen<(MAXGEN-1)):
		sObjV = np.sort(ObjV)
		best[gen] = np.min(ObjV)
		minimum = best[gen]
		mean_fits[gen] = np.mean(ObjV)
		worst[gen] = np.max(ObjV)

		#visualizeTSP(x,y,adj2path(Chrom(t,:)), minimum, ah1, gen, best, mean_fits, worst, ah2, ObjV, NIND, ah3);
		scDepth = 20
		scArgs = [best[:(gen+1)],scDepth,sObjV,stopN]
		stopCriteria = STOPCRITERIA(scArgs)
		if (stopCriteria):
		#if(sObjV[stopN]-sObjV[0]<(10**-5)):
			runData['BREAK'] = gen
			break
		# runData['GENERATIONAL_DATA'][gen]={}
		# runData['GENERATIONAL_DATA'][gen]['START_GENERATION_CHROMOSOMES'] = Chrom
		#assign fitness values to entire population
		FitnV = tsp_ranking.tsp_ranking(ObjV) 
		# runData['GENERATIONAL_DATA'][gen]['STARTING_FITNESS'] = ObjV
		#select individuals for breeding
		SelCh = tsp_select.tsp_select(SELECTION, Chrom, FitnV, GGAP)
		# runData['GENERATIONAL_DATA'][gen]['SELECTED_CHROMOSOMES'] = SelCh
		#recombine individuals (crossover)
		SelCh = tsp_recombin.tsp_recombin(CROSSOVER,SelCh,PR_CROSS)
		# runData['GENERATIONAL_DATA'][gen]['RECOMBINED_CHROMOSOMES'] = SelCh
		SelCh = tsp_mutate.tsp_mutate(MUTATION,SelCh,PR_MUT)
		# runData['GENERATIONAL_DATA'][gen]['MUTATED_CHROMOSOMES'] = SelCh
		#evaluate offspring, call objective function
		ObjVSel = tsp_fun.tsp_fun(SelCh,Dist)
		#reinsert offspring into population
		Chrom,ObjV = tsp_reins.tsp_reins(Chrom,SelCh,1,[1],ObjV,ObjVSel)
		# runData['GENERATIONAL_DATA'][gen]['REINSERTED_CHROMOSOMES'] = Chrom
	            
	#	Chrom = tsp_ImprovePopulation.tsp_ImprovePopulation(NIND, NVAR, Chrom, LOCALLOOP, Dist)
		#increment generation counter
		#gen+=1

	runData['RESULTS'] = {
		'BEST':best,
		'WORST':worst,
		'MEAN':mean_fits
	}
	return runData