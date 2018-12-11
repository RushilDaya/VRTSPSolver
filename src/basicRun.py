# simple run script to test out how data gets saved
# hard code data and configurations
# just for rapid testing

import pickle
import numpy as np
from run_ga import run_ga
from xalt_edges import xalt_edges

# every 

def load_data(fileName):
    # dummy function for now
    x = np.array([273.46509 367.34973 378.83914 225.10242 179.65437 272.98428 20.70829  31.18826 441.09842 215.28487 220.84784 153.61868 251.23114 339.36380 141.00000 143.00000])
    y = np.array([[204.95761, 5.14920, 86.38704, 170.73392 ,211.91306, 97.19602 , 227.85622, 25.77590, 162.63313, 30.03942, 112.75235, 31.05856, 240.80257, 209.36363,143.00000,85.00000])


    x = np.array([2,3,5,1,7,8,3,6,1,0,4,1])
    y = np.array([2,3,2,7,2,8,9,4,1,1,2,8])
    return x,y

def load_configurations(fileName):
    # dummy function for now
    return [{'NAME':'conf1','NIND':50,'MAXGEN':500,'ELITIST':0.5,'STOP_PERCENTAGE':1,'PR_CROSS':0.3,'PR_MUT':0.1,'LOCALLOOP':None,'CROSSOVER':xalt_edges}]

def runConfiguration(config,x,y, dataFile ,runsNum):
    print(config)
    outputFileName = dataFile.split('.')[0] + '_' + config['NAME'] + '.pkl'
    configObj = {}
    configObj['PARAMETERS']={
					'NIND':config['NIND'],
					'MAXGEN':config['MAXGEN'],
					'NVAR':len(x),
					'ELITIST':config['ELITIST'],
					'STOP_PERCENTAGE':config['STOP_PERCENTAGE'],
					'PR_CROSS':config['PR_CROSS'],
					'PR_MUT':config['PR_MUT'],
					'LOCALLOOP':config['LOCALLOOP']        
    }
    runs = []

    for i in range(runsNum):
        runData = run_ga(x,y, config['NIND'], config['MAXGEN'], len(x),
                         config['ELITIST'], config['STOP_PERCENTAGE'], config['PR_CROSS'],
                         config['PR_MUT'], config['CROSSOVER'], config['LOCALLOOP'])
        runs.append(runData)

    configObj['RUNS']=runs
    outFile = open(outputFileName,'wb')
    pickle.dump(configObj,outFile)
    outFile.close()

    return True


def main():
    DATA_NAME = 'customData.txt'
    configList = load_configurations('config.yaml')
    x,y = load_data(DATA_NAME)
    runsPerConfig = 5
    [ runConfiguration(configuration, x,y, DATA_NAME, runsPerConfig)  for configuration in configList] 
    

if __name__ == "__main__":
    main()
