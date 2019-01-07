# a test script to visual results and
# make sure the run pickles are working correctly

import pickle
import numpy as np
import math
import matplotlib.pyplot as plt
from plotRoute import plotRoute


def analyseRun(run):
    try:
        best = run['RESULTS']['BEST']
        worst = run['RESULTS']['WORST']
        mean = run['RESULTS']['MEAN']
        x=np.linspace(1,len(best),len(best))
        plt.plot(x,best, color='r')
        plt.plot(x,mean, color='b')
        plt.plot(x,worst, color='g')
        plt.show()
    except:
        pass

    
def analyseBestPath(run, representation,x,y):
    try:
        best = run['FINAL_CHROMOSOME'][run['FINAL_FITNESS'].argmin()]
        plotRoute(x,y,best, representation)
    except:
        pass



def heatmap(run):
    try:
        genData = run['GENERATIONAL_DATA']
        numRuns = max(genData.keys())
        allFitness = []
        for i in range(numRuns+1):
            allFitness.append(genData[i]['FITNESS'].tolist())

        # get absolute worst fitness
        leastFit = max([ max(item) for item in allFitness ])
        mostFit  = min([ min(item) for item in allFitness ])


        # create buckets equal to number of individuals
        buckets = np.linspace(mostFit,leastFit, len(allFitness[0]))

        bucketIncrement = buckets[1]-buckets[0]

        heat = np.zeros([len(buckets),numRuns])
        

        for i in range(numRuns):
            generationalFitness  = allFitness[i]
            for j in range(len(generationalFitness)):
                bucket_index = math.floor( (mostFit - generationalFitness[j])/bucketIncrement)
                heat[bucket_index,i] = heat[bucket_index,i]+1

        plt.imshow(heat, cmap='hot', interpolation='nearest',aspect='auto')
        plt.show()
    except:
        pass

def checkResults(fileName):
    fileData = open(fileName,'rb')
    confObjList = pickle.load(fileData)
    for confObj in  confObjList:
        print(confObj, confObjList[confObj]['PARAMETERS']['IMPROVE_POP'])
        representation = confObjList[confObj]['PARAMETERS']['REPRESENTATION']
        runs = confObjList[confObj]['RUNS']
        x = confObjList[confObj]['NODES']['X']
        y = confObjList[confObj]['NODES']['Y']
        [(analyseRun(run), heatmap(run) ,analyseBestPath(run, representation, x,y)) for run in runs]

    return True

while True:
    fileToAnalize = input('enter file name:')
    fileToAnalize = '../resources/out/'+fileToAnalize+'.pkl'
    checkResults(fileToAnalize)