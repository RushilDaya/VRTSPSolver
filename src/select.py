import numpy as np

# This function performs universal selection. The function handles
# multiple populations and calls the low level selection function
# for the actual selection process.

def select(SEL_F, Chrom, FitnV, GGAP = 1.0, SUBPOP = 1):
    #Identify the population size (Nind)
    #Chrom is a matrix
    #FitnV is an array
    NindCh,Nvar = Chrom.shape
    NindF = len(FitnV)

    if (NindCh != NindF):
        raise disagree('Chrom and FitnV disagree')
    if (GGAP < 0):
        error('GGAP must be a scalar bigger than 0'); end
    if ((NindCh/SUBPOP) != np.fix(NindCh/SUBPOP)).all():
        raise disagree('Chrom and SUBPOP disagree')
    Nind = NindCh/SUBPOP  #Compute number of individuals per subpopulation

    # Compute number of new individuals (to select)
    NSel = max(np.floor(Nind*GGAP+0.5),2)
    
    # Select individuals from population
    SelCh = None
    for irun in range(SUBPOP):
        FitnVSub = FitnV[int((irun)*Nind):int((irun+1)*Nind)]
        ChrIx = SEL_F(FitnVSub, NSel)+(irun*Nind)
        ChrIx = ChrIx.astype('int')
        
        if type(SelCh) != np.matrixlib.defmatrix.matrix:
            SelCh = Chrom[ChrIx]
        else:
            SelCh = np.append(SelCh,Chrom[ChrIx],axis=0)
            
    return SelCh