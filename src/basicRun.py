# simple run script to test out how data gets saved
# hard code data and configurations
# just for rapid testing

import pickle
import numpy as np
import inputData
import tsp_crossoverMethods
from tsp_runGA import tsp_runGA
import tsp_crossoverMethods, tsp_mutationMethods, tsp_selectionMethods, tsp_reinsMethods, tsp_improvePopulationMethods

# every 

def load_data(fileName):
    # dummy function for now
    #x = np.array([273.46509, 367.34973, 378.83914, 225.10242, 179.65437, 272.98428, 20.70829,  31.18826, 441.09842, 215.28487, 220.84784, 153.61868, 251.23114, 339.36380, 141.00000, 143.00000])
    #y = np.array([204.95761, 5.14920, 86.38704, 170.73392 ,211.91306, 97.19602 , 227.85622, 25.77590, 162.63313, 30.03942, 112.75235, 31.05856, 240.80257, 209.36363,143.00000,85.00000])
    return inputData.inputData(fileName)

def load_configurations(fileName):
    # dummy function for now
    return [{'NAME':'conf1', 'REPRESENTATION':'REP_PATH',
             'NIND':50,'MAXGEN':25,
             'STOP_PERCENTAGE':1,'PR_CROSS':0.95,
             'PR_MUT':1.0,'IMPROVE_POP':tsp_improvePopulationMethods.tsp_improvePath,
             'CROSSOVER':tsp_crossoverMethods.tsp_sequentialConstructiveCrossover,
             'MUTATION':tsp_mutationMethods.tsp_inversion,
             'SELECTION':tsp_selectionMethods.tsp_sus,
             'REINSERTION':tsp_reinsMethods.tsp_genitor,
             'OFFSPRING_FACTOR':2.0,
             'ELITE_PERCENTAGE':0.1
             }]


def runConfiguration(config,x,y, dataFile ,runsNum):
    print(config)
    outputFileName = 'withNone.pkl'
    configObj = {}
    configObj['PARAMETERS']={
                    'REPRESENTATION':config['REPRESENTATION'],
					'NIND':config['NIND'],
					'MAXGEN':config['MAXGEN'],
					'NVAR':len(x),
                    'OFFSPRING_FACTOR':config['OFFSPRING_FACTOR'],
					'ELITE_PERCENTAGE':config['ELITE_PERCENTAGE'],
					'STOP_PERCENTAGE':config['STOP_PERCENTAGE'],
					'PR_CROSS':config['PR_CROSS'],
					'PR_MUT':config['PR_MUT'],
					'IMPROVE_POP':config['IMPROVE_POP']        
    }
    runs = []

    for i in range(runsNum):
        runData = tsp_runGA(config['REPRESENTATION'], x,y, config['NIND'],config['OFFSPRING_FACTOR'] ,config['MAXGEN'], len(x),
                         config['ELITE_PERCENTAGE'], config['STOP_PERCENTAGE'], config['PR_CROSS'],
                         config['PR_MUT'], config['CROSSOVER'], config['MUTATION'], config['SELECTION'],config['REINSERTION'], config['IMPROVE_POP'])
        runs.append(runData)

    configObj['RUNS']=runs
    outFile = open(outputFileName,'wb')
    pickle.dump(configObj,outFile)
    outFile.close()

    return True


def main():
    DATA_NAME = '../resources/datasets/rondrit127.tsp'
    configList = load_configurations('config.yaml')
    x,y = load_data(DATA_NAME)
    runsPerConfig = 1
    [ runConfiguration(configuration, x,y, DATA_NAME, runsPerConfig)  for configuration in configList] 
    

if __name__ == "__main__":
    main()
