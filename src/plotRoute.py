# simple ploting function which 
# for drawing the path through nodes

import matplotlib.pyplot as plt 
import numpy as np 

def plot(nodes,pathRep):
        # nodes is a N by 2 matrix
        # pathRep is an array in the PATH REPRESENTATION
    NVAR = len(pathRep)
    for i in range(NVAR-1):
        x1 = nodes[pathRep[i]-1,0]
        y1 = nodes[pathRep[i]-1,1]
        x2 = nodes[pathRep[i+1]-1,0]
        y2 = nodes[pathRep[i+1]-1,1]
        x = [x1,x2]
        y = [y1,y2]
        plt.plot(x,y,marker='o',color='r')
    plt.plot([nodes[pathRep[-1]-1,0],nodes[pathRep[0]-1,0]],[nodes[pathRep[-1]-1,1],nodes[pathRep[0]-1,1]],marker='o',color='b')
    plt.show()