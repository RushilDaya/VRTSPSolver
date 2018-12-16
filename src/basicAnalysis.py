# a test script to visual results and
# make sure the run pickles are working correctly

import pickle
import numpy as np
import matplotlib.pyplot as plt
from plotRoute import plotRoute


def analyseRun(run):
    best = run['RESULTS']['BEST']
    worst = run['RESULTS']['WORST']
    mean = run['RESULTS']['MEAN']
    x=np.linspace(1,len(best),len(best))
    plt.plot(x,best, color='r')
    plt.plot(x,mean, color='b')
    plt.plot(x,worst, color='g')
    plt.show()
    
def analyseBestPath(run, representation):
    genData = run['GENERATIONAL_DATA']
    lastRun = max(genData.keys())
    best = genData[lastRun]['START_GENERATION_CHROMOSOMES'][genData[lastRun]['STARTING_FITNESS'].argmin()]
    plotRoute(run['NODES']['X'],run['NODES']['Y'],best, representation)



def checkResults(fileName):
    fileData = open(fileName,'rb')
    confObj = pickle.load(fileData)
    print(confObj['PARAMETERS'])
    representation = confObj['PARAMETERS']['REPRESENTATION']
    runs = confObj['RUNS']
    [(analyseRun(run),analyseBestPath(run, representation)) for run in runs]

    return True

while True:
    fileToAnalize = input('enter file name:')
    checkResults(fileToAnalize)