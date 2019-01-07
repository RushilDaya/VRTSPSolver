import time, glob, yaml, pickle
import inputData
import numpy as np
import matplotlib.pyplot as plt
from tsp_runGA import tsp_runGA
import tsp_crossoverMethods, tsp_mutationMethods, tsp_selectionMethods, tsp_reinsMethods, tsp_improveMethods, tsp_stopCriteria
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

def _configParams(cfg,currentConfig,pathFile ):
	REPRESENTATION = cfg[currentConfig]['REPRESENTATION']

	# MAPPING
	mutation_mappings = tsp_mutationMethods.mapping()
	crossover_mappings = tsp_crossoverMethods.mapping(REPRESENTATION)
	selection_mappings = tsp_selectionMethods.mapping(REPRESENTATION)
	reinsertion_mappings = tsp_reinsMethods.mapping()
	improvement_mappings = tsp_improveMethods.mapping()
	stopCriteria_mapping = tsp_stopCriteria.mapping()

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
	STOPCRITERIA = cfg[currentConfig]['STOPCRITERIA']
	STOPCRITERIA = stopCriteria_mapping[STOPCRITERIA]
	RANKBASE = cfg[currentConfig]['RANKBASE']

	x,y = inputData.inputData(pathFile)
	NVAR = len(x)

	return [REPRESENTATION, x, y, NIND, OFFSPRING_FACTOR, MAXGEN, NVAR, ELITE_PERCENTAGE, STOP_PERCENTAGE, PR_CROSS, PR_MUT, CROSSOVER, MUTATION, SELECTION,STOPCRITERIA,REINSERTION ,IMPROVE_POP, RANKBASE]
################################################################################################################################################################################################

# PATHS
pathCnf = '../resources/'
pathData = '../resources/datasets/'

# VARS
N_CORES = 4
REPETITIONS = 1
fileName = 'rondrit016.tsp'

# FUNCTIONS
def _runGAByProccess(argsTSP):
	REPRESENTATION, x, y, NIND, OFFSPRING_FACTOR, MAXGEN, NVAR, ELITE_PERCENTAGE, STOP_PERCENTAGE, PR_CROSS, PR_MUT, CROSSOVER, MUTATION, SELECTION,STOPCRITERIA,REINSERTION ,IMPROVE_POP, RANKBASE= argsTSP
	res = tsp_runGA(REPRESENTATION,x, y, NIND, OFFSPRING_FACTOR, MAXGEN, NVAR, ELITE_PERCENTAGE, STOP_PERCENTAGE, PR_CROSS, PR_MUT, CROSSOVER, MUTATION, SELECTION,STOPCRITERIA,REINSERTION ,IMPROVE_POP, RANKBASE=RANKBASE)
	return res

def _mp(func, args, cores, currentConfig):
	with ProcessPoolExecutor(max_workers=cores) as executor:
		res = executor.map(func, args)
	#print(currentConfig,list(res))
	return list(res)


# MAIN SCRIPT
with open(pathCnf+"config.yml") as ymlfile:
		cfg = yaml.load(ymlfile)

start_time = time.time()
configGeneral = {}
keys = list(cfg.keys())
idx=0
#mutationsMethods = ['tsp_inversion', 'tsp_swap', 'tsp_nSwap', 'tsp_insertion', 'tsp_scramble', 'tsp_3scramble']
#selectionMethods = ['tsp_sus','tsp_fps','tsp_deterministic_tournament','tsp_nondeterministic_tournament','tsp_nondeterministic_tournament_battle','tsp_rankLinear','tsp_rankExponential']
for currentConfig in keys:
	if (idx%1==0):
		print(idx,': ',time.strftime("%H:%M:%S"), 'Delta:',time.strftime('%H:%M:%S', time.gmtime((time.time() - start_time))))
	idx+=1
	##SET PARAMETERS
	argsTSP = _configParams(cfg, currentConfig, pathData+fileName)

	##Multiprocess GA Run
	res = _mp(_runGAByProccess, [argsTSP for i in range(REPETITIONS)], N_CORES, currentConfig)
	
	## Write to File Output res
	##########################
	REPRESENTATION, x, y, NIND, OFFSPRING_FACTOR, MAXGEN, NVAR, ELITE_PERCENTAGE, STOP_PERCENTAGE, PR_CROSS, PR_MUT, CROSSOVER, MUTATION, SELECTION,STOPCRITERIA,REINSERTION ,IMPROVE_POP, RANKBASE= argsTSP
	
	configObj = {}
	configObj['PARAMETERS']={
		'REPRESENTATION':REPRESENTATION,
		'NIND':NIND,
		'MAXGEN':MAXGEN,
		'NVAR':NVAR,
		'ELITE_PERCENTAGE':ELITE_PERCENTAGE,
		'STOP_PERCENTAGE':STOP_PERCENTAGE,
		'PR_CROSS':PR_CROSS,
		'PR_MUT':PR_MUT,
		'OFFSPRING_FACTOR':OFFSPRING_FACTOR,
		'CROSSOVER':CROSSOVER.__name__, 
		'MUTATION':MUTATION.__name__, 
		'SELECTION':SELECTION.__name__,
		'STOPCRITERIA':STOPCRITERIA.__name__,
		'REINSERTION':REINSERTION.__name__,
		'IMPROVE_POP':IMPROVE_POP.__name__, 
		'RANKBASE':RANKBASE
	}
	Nodes={}
	Nodes['X']=x
	Nodes['Y']=y
	configObj['NODES'] = Nodes
	configObj['RUNS'] = res  
	configGeneral[currentConfig] = configObj

outputFileName = '../resources/out/'+fileName[:-4]+'.pkl'
outFile = open(outputFileName,'wb')
pickle.dump(configGeneral,outFile)
outFile.close()

print(idx,': ',time.strftime("%H:%M:%S"))
print(time.strftime('%H:%M:%S', time.gmtime((time.time() - start_time))))
print('DONE!')
