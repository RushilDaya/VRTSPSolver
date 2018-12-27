# simple ploting function which 
# for drawing the path through nodes

import matplotlib.pyplot as plt 
import numpy as np 
from tsp_adj2path import tsp_adj2path

def plotRoute(nodesX,nodesY,pathRep, REPRESENTATION):
        # nodes is a N by 2 matrix
        # pathRep is an array in the Adjacency
  #  pathRep = tsp_adj2path(pathRep.tolist()[0])
    if REPRESENTATION == 'REP_PATH':
        pathRep = pathRep.tolist()[0]
    elif REPRESENTATION == 'REP_ADJACENCY':
        pathRep = tsp_adj2path(pathRep.tolist()[0])
        
    NVAR = len(pathRep)
    for i in range(NVAR-1):
        x1 = nodesX[pathRep[i]-1]
        y1 = nodesY[pathRep[i]-1]
        x2 = nodesX[pathRep[i+1]-1]
        y2 = nodesY[pathRep[i+1]-1]
        x = [x1,x2]
        y = [y1,y2]
        plt.plot(x,y,marker='o',color='r')
    plt.plot([nodesX[pathRep[-1]-1],nodesX[pathRep[0]-1]],[nodesY[pathRep[-1]-1],nodesY[pathRep[0]-1]],marker='o',color='b')
    plt.show()