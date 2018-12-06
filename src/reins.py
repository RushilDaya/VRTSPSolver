import numpy as np

# REINS.M        (RE-INSertion of offspring in population replacing parents)
# This function reinserts offspring in the population.

def reins(Chrom, SelCh, SUBPOP = 1, InsOpt = None, ObjVCh = None, ObjVSel = None):

# Check parameter consistency
	NindP, NvarP = Chrom.shape
	NindO, NvarO = SelCh.shape

	if ((NindP/SUBPOP) != np.fix(NindP/SUBPOP)).all():
		raise disagree('Chrom and SUBPOP disagree')
	if ((NindO/SUBPOP) != np.fix(NindO/SUBPOP)).all():
		raise disagree('SelCh and SUBPOP disagree')

	NIND = NindP//SUBPOP  # Compute number of individuals per subpopulation
	NSEL = NindO//SUBPOP  # Compute number of offspring per subpopulation


   if ObjVCh:
		mO, nO = ObjVCh.shape
		if (nO != 1):
			raise dimension('ObjVCh must be a column vector')
		if (NindO != mO):
			raise disagree('Chrom and ObjVCh disagree')

	if ObjVSel:
		mO, nO = ObjVSel.shape
		if (nO != 1):
			raise dimension('ObjVSel must be a column vector')
		if (NindO != mO):
			raise disagree('SelCh and ObjVSel disagree')

	INSR = 1.0
	Select = 0
	if InsOpt:
		if (len(InsOpt) > 2):
			raise dimension('Parameter InsOpt too long')
		if (len(InsOpt) >= 1):
			Select = InsOpt(0)
		if (len(InsOpt) >= 2):
			INSR = InsOpt(1)

	if (INSR < 0 | INSR > 1):
		raise range('Parameter for insertion rate must be a scalar in [0, 1]')
	if (INSR < 1 and not(ObjVSel)):
		raise dimension('For selection of offspring ObjVSel is needed')
	if (Select != 0 and Select != 1):
		raise range('Parameter for selection method must be 0 or 1')
	if (Select and not(ObjVCh)):
		raise dimension('ObjVCh for fitness-based exchange needed')

	if not(INSR):
		return

	NIns = min(max(np.floor(INSR*NSEL+0.5),1),NIND)	# Number of offspring to insert   


	# perform insertion for each subpopulation
	for irun in range(SUBPOP):
		# Calculate positions in old subpopulation, where offspring are inserted
		if (Select):	# fitness-based reinsertion
			tmp = ObjVCh[(irun)*NIND:((irun+1)*NIND)]
			ChIx = np.argsort(-tmp)
		else:				# uniform reinsertion
			ChIx = np.argsort(np.array([random.random() for x in range(NIND)]))

		PopIx = ChIx(0:NIns) + (irun)*NIND
		# Calculate position of Nins-% best offspring
		if (NIns < NSEL):  # select best offspring
			tmp = ObjVSel((irun) * NSEL:(irun+1)*NSEL)
			OffIx = np.argsort(tmp)
		else:              
			OffIx = range(NIns)

		SelIx = OffIx(0:NIns) + (irun)*NSEL
		# Insert offspring in subpopulation -> new subpopulation
		Chrom[PopIx] = SelCh[SelIx]

		if (ObjVCh and ObjVSel):
			ObjVCh(PopIx) = ObjVSel(SelIx)

return Chrom, ObjVCh