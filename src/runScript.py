import yaml
import pickle
import inputData
import numpy as np
from tsp_runGA import tsp_runGA
import tsp_crossoverMethods, tsp_mutationMethods, tsp_selectionMethods, tsp_reinsMethods, tsp_improvePopulationMethods, tsp_stopCriteria
from concurrent.futures import ProcessPoolExecutor

# CONSTANTS
N_CORES = 4
REPETITIONS = 3

# MAPPING
mutation_mappings = tsp_mutationMethods.mapping()
crossover_mappings = tsp_crossoverMethods.mapping('REP_ADJACENCY')
selection_mappings = tsp_selectionMethods.mapping('REP_ADJACENCY')
reinsertion_mappings = tsp_reinsMethods.mapping()
improvement_mappings = tsp_improvePopulationMethods.mapping()
stopCriteria_mapping = tsp_stopCriteria.mapping()

# PATHS
pathCnf = '../resources/'
pathData = '../resources/datasets/'

# FUNCTIONS
def runGAByProccess(argsTSP):
	REPRESENTATION,x, y, NIND, OFFSPRING_FACTOR, MAXGEN, NVAR, ELITE_PERCENTAGE, STOP_PERCENTAGE, PR_CROSS, PR_MUT, CROSSOVER, MUTATION, SELECTION,STOPCRITERIA,REINSERTION ,IMPROVE_POP = argsTSP
	res = tsp_runGA(REPRESENTATION,x, y, NIND, OFFSPRING_FACTOR, MAXGEN, NVAR, ELITE_PERCENTAGE, STOP_PERCENTAGE, PR_CROSS, PR_MUT, CROSSOVER, MUTATION, SELECTION,STOPCRITERIA,REINSERTION ,IMPROVE_POP)
	return res

def mp(func, args, cores, currentConfig):
	with ProcessPoolExecutor(max_workers=cores) as executor:
		res = executor.map(func, args)
	return list(res)


# MAIN SCRIPT
with open(pathCnf+"config.yml") as ymlfile:
		cfg = yaml.load(ymlfile)


keys = list(cfg.keys())
dataFiles = ['rondrit048.tsp']

for currentConfig in keys:
	for fileName in dataFiles:

		outputFileName = '../resources/out/'+currentConfig+'_'+fileName.split('.')[0]+'.pkl'

		##SET PARAMETERS
		############################################################
		REPRESENTATION = cfg[currentConfig]['REPRESENTATION']
		NIND = cfg[currentConfig]['NIND']
		OFFSPRING_FACTOR = cfg[currentConfig]['OFFSPRING_FACTOR']
		MAXGEN = cfg[currentConfig]['MAXGEN']
		ELITE_PERCENTAGE = cfg[currentConfig]['ELITE_PERCENTAGE']
		STOP_PERCENTAGE = cfg[currentConfig]['STOP_PERCENTAGE']
		PR_CROSS = cfg[currentConfig]['PR_CROSS']
		PR_MUT = cfg[currentConfig]['PR_MUT']
		CROSSOVER = cfg[currentConfig]['CROSSOVER']
		CROSSOVER = crossover_mappings[CROSSOVER]
		MUTATION = cfg[currentConfig]['MUTATION']
		MUTATION = mutation_mappings[MUTATION]
		SELECTION = cfg[currentConfig]['SELECTION']
		SELECTION = selection_mappings[SELECTION]
		REINSERTION = cfg[currentConfig]['REINSERTION']
		REINSERTION = reinsertion_mappings[REINSERTION]
		IMPROVE_POP = cfg[currentConfig]['IMPROVE_POP']
		IMPROVE_POP = improvement_mappings[IMPROVE_POP]
		STOPCRITERIA = cfg[currentConfig]['STOPCRITERIA']
		if STOPCRITERIA=='bestWorst':
			tsp_stopCriteria.setThreshold((10**-1))
		elif STOPCRITERIA=='stdDev':
			tsp_stopCriteria.setThreshold((10**-1.7))
		elif STOPCRITERIA=='phi':
			tsp_stopCriteria.setThreshold((0.14))
		elif STOPCRITERIA=='runingMean':
			tsp_stopCriteria.setThreshold((10**-6))
		else:
			tsp_stopCriteria.setThreshold(0)

		STOPCRITERIA = stopCriteria_mapping[STOPCRITERIA]

		x,y = inputData.inputData(pathData+fileName)
		NVAR = len(x)
		############################################################

		##Multiprocess GA Run
		argsTSP = [REPRESENTATION,x, y, NIND, OFFSPRING_FACTOR, MAXGEN, NVAR, ELITE_PERCENTAGE, STOP_PERCENTAGE, PR_CROSS, PR_MUT, CROSSOVER, MUTATION, SELECTION,STOPCRITERIA,REINSERTION ,IMPROVE_POP]
		print (argsTSP)
		res = mp(runGAByProccess, [argsTSP for i in range(REPETITIONS)], N_CORES, currentConfig)
		#print (res)
		## Write to File Output res
		##########################
			
		configObj = {}
		configObj['NODES']={
			'X':x,
			'Y':y
		}

		configObj['PARAMETERS']={
			'REPRESENTATION':REPRESENTATION,
			'NIND':NIND,
			'OFFSPRING_FACTOR':OFFSPRING_FACTOR,
			'MAXGEN':MAXGEN,
			'NVAR':len(x),
			'ELITE_PERCENTAGE':ELITE_PERCENTAGE,
			'STOP_PERCENTAGE':STOP_PERCENTAGE,
			'PR_CROSS':PR_CROSS,
			'PR_MUT':PR_MUT,
			'STOPCRITERIA':STOPCRITERIA.__name__,
			'REINSERTION':REINSERTION.__name__,
			'IMPROVE_POP':IMPROVE_POP.__name__,
			'CROSSOVER':CROSSOVER.__name__,
			'MUTATION':MUTATION.__name__,
			'SELECTION':SELECTION.__name__

		}
		configObj['RUNS']=res
		outFile = open(outputFileName,'wb')
		pickle.dump(configObj,outFile)
		outFile.close()
