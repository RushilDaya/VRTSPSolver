import numpy as np

# This function performs universal selection. The function handles
# multiple populations and calls the low level selection function
# for the actual selection process.

def select(SEL_F, Chrom, FitnV, GGAP = 1.0, SUBPOP = 1):
	#Identify the population size (Nind)
	
	NindCh,Nvar = Chrom.shape
	NindF,VarF = FitnV.shape

	if (NindCh ~= NindF):
		raise disagree('Chrom and FitnV disagree')
	if (VarF != 1):
		raise dimension('FitnV must be a column vector')
	if (GGAP < 0):
		  error('GGAP must be a scalar bigger than 0'); end
	if ((Nind/SUBPOP) != np.fix(Nind/SUBPOP)).all():
		raise disagree('Chrom and SUBPOP disagree')
	Nind = Nind/SUBPOP  #Compute number of individuals per subpopulation
	
	# Compute number of new individuals (to select)
	NSel = max(np.floor(Nind*GGAP+0.5),2)

	# Select individuals from population
	SelCh = np.matrix([])
	for irun in range(SUBPOP):
		FitnVSub = FitnV[(irun)*Nind+1:(irun+1)*Nind]
		ChrIx = SEL_F(FitnVSub, NSel)+(irun*Nind)
		SelCh = numpy.concatenate((SelCh, Chrom[ChrIx:]))	 

return SelCh