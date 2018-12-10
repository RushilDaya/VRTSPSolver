import numpy as np

# This function performs recombination between pairs of individuals
# and returns the new individuals after mating. The function handles
# multiple populations and calls the low-level recombination function
# for the actual recombination process.

def tsp_recombin(REC_F, Chrom, RecOpt = 0.7, SUBPOP = 1):

   if (RecOpt < 0 or RecOpt > 1):
      raise outOfRange("RecOpt must be a scalar in [0, 1]")
   
   # Identify the population size (Nind)
   Nind, Nvar = Chrom.shape

   if ((Nind/SUBPOP) != np.fix(Nind/SUBPOP)).all():
      raise disagree('Chrom and SUBPOP disagree')
   Nind = Nind//SUBPOP  #Compute number of individuals per subpopulation
   
   # Select individuals of one subpopulation and call low level function
   
   NewChrom = None
   for irun in range(SUBPOP):
      ChromSub = Chrom[(irun)*Nind+1:(irun+1)*Nind]
      NewChromSub = REC_F(ChromSub, RecOpt);
      NewChrom = NewChrom and numpy.concatenate((NewChrom, NewChromSub)) or np.copy(NewChromSub)
   
   return np.matrix(NewChrom)