import numpy as np

# This function performs universal selection. The function handles
# multiple populations and calls the low level selection function
# for the actual selection process.

def tsp_select(SEL_F, Chrom, FitnV, OFFSPRING_FACTOR = 1.0, SUBPOP = 1):
	#Identify the population size (Nind)
	#Chrom is a matrix
	#FitnV is an array
	NindCh,Nvar = Chrom.shape
	NindF = len(FitnV)

	if (NindCh != NindF):
		raise disagree('Chrom and FitnV disagree')
	if (OFFSPRING_FACTOR < 0):
		error('OFFSPRING_FACTOR must be a scalar bigger than 0'); end
	if ((NindCh/SUBPOP) != np.fix(NindCh/SUBPOP)).all():
		raise disagree('Chrom and SUBPOP disagree')
	Nind = NindCh//SUBPOP  #Compute number of individuals per subpopulation

	# Compute number of new individuals (to select)
	NSel = max(np.floor(Nind*OFFSPRING_FACTOR+0.5),2)
	
	# Select individuals from population
	SelCh = None
	for irun in range(SUBPOP):
		FitnVSub = FitnV[int((irun)*Nind):int((irun+1)*Nind)]
		ChrIx = SEL_F(FitnVSub, NSel)+(irun*Nind)
		ChrIx = ChrIx.astype('int')
		
		SelCh = SelCh and np.append(SelCh,Chrom[ChrIx],axis=0) or Chrom[ChrIx]
			
	return np.matrix(SelCh)