# a test script to visual results and
# make sure the run pickles are working correctly

import pickle
import numpy as np
import matplotlib.pyplot as plt

def analyseRun(run):
    best = run['RESULTS']['BEST']
    worst = run['RESULTS']['WORST']
    mean = run['RESULTS']['MEAN']
    x=np.linspace(1,len(best),len(best))
    plt.plot(x,best, color='r')
    plt.plot(x,mean, color='b')
    plt.plot(x,worst, color='g')
    plt.show()
    

def checkResults(fileName):
    fileData = open(fileName,'rb')
    confObj = pickle.load(fileData)
    print(confObj['PARAMETERS'])
    runs = confObj['RUNS']
    [analyseRun(run) for run in runs]
    return True

while True:
    fileToAnalize = input('enter file name:')
    checkResults(fileToAnalize)