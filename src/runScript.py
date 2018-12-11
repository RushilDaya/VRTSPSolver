import yaml
import inputData
import numpy as np
from tsp_runGA import tsp_runGA
import tsp_crossoverMethods, tsp_mutationMethods, tsp_selectionMethods
from concurrent.futures import ProcessPoolExecutor

# CONSTANTS
N_CORES = 4
N_THREADS = 2
REPETITIONS = 300

# MAPPING
mutation_mappings = tsp_mutationMethods.mapping()
crossover_mappings = tsp_crossoverMethods.mapping('REP_ADJACENCY')
selection_mappings = tsp_selectionMethods.mapping('REP_ADJACENCY')

# PATHS
pathCnf = '../resources/'
pathData = '../resources/datasets/'

# FUNCTIONS
def runGAByProccess(argsTSP):
	x, y, NIND, MAXGEN, NVAR, ELITIST, STOP_PERCENTAGE, PR_CROSS, PR_MUT, CROSSOVER, MUTATION, SELECTION, LOCALLOOP = argsTSP
	res = tsp_runGA(x, y, NIND, MAXGEN, NVAR, ELITIST, STOP_PERCENTAGE, PR_CROSS, PR_MUT, CROSSOVER, MUTATION, SELECTION, LOCALLOOP)
	return res

def mp(func, args, cores, currentConfig):
	with ProcessPoolExecutor(max_workers=cores) as executor:
		res = executor.map(func, args)
	#print(currentConfig,list(res))
	return list(res)


# MAIN SCRIPT

with open(pathCnf+"config.yml") as ymlfile:
		cfg = yaml.load(ymlfile)


keys = list(cfg.keys())
fileName = 'rondrit004.tsp'
for currentConfig in keys:
	##SET PARAMETERS
	############################################################
	NIND = cfg[currentConfig]['NIND']
	MAXGEN = cfg[currentConfig]['MAXGEN']
	ELITIST = cfg[currentConfig]['ELITIST']
	#GGAP = 1-ELITIST
	STOP_PERCENTAGE = cfg[currentConfig]['STOP_PERCENTAGE']
	PR_CROSS = cfg[currentConfig]['PR_CROSS']
	PR_MUT = cfg[currentConfig]['PR_MUT']
	LOCALLOOP = cfg[currentConfig]['LOCALLOOP']
	CROSSOVER = cfg[currentConfig]['CROSSOVER']
	CROSSOVER = crossover_mappings[CROSSOVER]
	MUTATION = cfg[currentConfig]['MUTATION']
	MUTATION = mutation_mappings[MUTATION]
	SELECTION = cfg[currentConfig]['SELECTION']
	SELECTION = selection_mappings[SELECTION]

	x,y = inputData.inputData(pathData+fileName)
	NVAR = len(x)
	############################################################

	##Multiprocess GA Run
	argsTSP = [x, y, NIND, MAXGEN, NVAR, ELITIST, STOP_PERCENTAGE, PR_CROSS, PR_MUT, CROSSOVER, MUTATION, SELECTION, LOCALLOOP]
	print (argsTSP)
	res = mp(runGAByProccess, [argsTSP for i in range(REPETITIONS)], N_CORES, currentConfig)
	## Write to File Output res
	##########################