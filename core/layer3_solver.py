import numpy as np
from core.layer2_solver import layer2Solver
import os
import glob

class layer3Solver(layer2Solver):
	def __init__(self,faces):
		super().__init__(faces)
		self.getOLLcases()
		self.getPLLcases()

	def getOLLcases(self):
		loc = os.getcwd() + '/OLL'
		self.loc = loc
		oll_files = [file for file in glob.glob(loc+"**/*.npz", recursive = True)]
		cases = []
		algos = []
		for fname in oll_files:
		    data = np.load(fname)
		    cases.append(data["arr_0"])
		    try:
		    	algos.append([rot.decode('utf-8') for rot in data["arr_1"]])
		    except:
		    	algos.append(data["arr_1"])
		self.oll_cases = cases
		self.oll_algos = algos

	def getPLLcases(self):
		pass

	def findTopMat(self):
	    nfaces = self.return2DFaces()
	    nfaces = sorted(nfaces,key=lambda x:x[1][1], reverse = False)

	    cmat = np.ones((5,5))
	    cmat[1:-1,1:-1] = nfaces[0]
	    cmat[1:-1,0] = nfaces[1][0,:]
	    cmat[1:-1,4] = nfaces[4][0,:][::-1]
	    cmat[0,1:-1] = nfaces[3][0,:][::-1]
	    cmat[4,1:-1] = nfaces[2][0,:]
	    
	    nmat = [[1 if col==0 else 0 for col in row] for row in cmat]
	    nmat[0][0] = 0; nmat[0][4] = 0; nmat[4][0] = 0; nmat[4][4] = 0
	    return nmat,cmat

	def findCase(self):
	    for i in range(4):
	        mat = self.findTopMat()[0]
	        for i in range(len(self.oll_cases)):
	            case = self.oll_cases[i]
	            if all((case == mat).reshape(25,1)):
	                return i
	        self.U()
	    raise Exception("Case not found")

	def runOLLsolver(self):
		self.runLayer2Solver()
		ind = self.findCase()
		for rot in self.oll_algos[ind]:
			self.rotation_dict[rot](self)
		topside = self.return2DFaces()[0]
		if all((topside==np.zeros((3,3))).reshape(9,1)):
			print("OLL done")
			self.compressAlgo()
			return

