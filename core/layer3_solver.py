import numpy as np
from core.layer2_solver import layer2Solver
import os
import glob

class layer3Solver(layer2Solver):
	def __init__(self,faces):
		super().__init__(faces)
		self.loc = os.getcwd()
		self.getOLLcases()
		self.getPLLcases()		 

	def getOLLcases(self):
		loc = self.loc + '/OLL'
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
		loc = self.loc + '/PLL'
		pll_files = [file for file in glob.glob(loc+"**/*.npz", recursive = True)]
		cases = []
		algos = []
		for fname in pll_files:
		    data = np.load(fname)
		    cases.append(data["arr_0"])
		    try:
		        algos.append([rot.decode('utf-8') for rot in data["arr_1"]])
		    except:
		        algos.append(data["arr_1"])
		self.pll_cases = cases
		self.pll_algos = algos

	def getOLLmatrix(self):
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

	def findOLLcase(self):
	    for i in range(4):
	        mat = self.getOLLmatrix()[0]
	        for i in range(len(self.oll_cases)):
	            case = self.oll_cases[i]
	            if all((case == mat).reshape(25,1)):
	                return i
	        self.U()
	    raise Exception("OLL Case not found")

	def runOLLsolver(self):
		self.runLayer2Solver()
		ind = self.findOLLcase()
		for rot in self.oll_algos[ind]:
			self.rotation_dict[rot](self)
		topside = self.return2DFaces()[0]
		if all((topside==np.zeros((3,3))).reshape(9,1)):
			return
		else:
			raise Exception("Incorrect OLL agorithm in database")

	def getPLLmatrix(self):
	    faces = self.return2DFaces()
	    back = faces[3][0][::-1]
	    left = faces[1][0]
	    front = faces[2][0]
	    right = faces[4][0][::-1]

	    piece_mat = np.array([[ (left[0],back[0]), (back[1]), (back[2],right[0])    ],\
	                 		  [ (left[1]),            (-1),       (right[1])        ],\
	                          [ (front[0],left[2]), (front[1]), (right[2],front[2]) ]])
	    solved_mat = np.array([[ (1,3), (3), (3,4) ],\
	                           [ (1),  (-1), (4) ],\
	                           [ (2,1), (2), (4,2) ]])

	    return piece_mat,solved_mat

	def rotPLLmatrix(self,piece_mat,formula):
	    piece_mat = piece_mat.reshape(9,1)
	    new_mat = piece_mat.copy()
	    for tup in formula:
	        i,j = tup
	        new_mat[j-1] = piece_mat[i-1]
	    return new_mat.reshape(3,3)

	def findPLLcase(self):
	    for i in range(len(self.pll_cases)):
	        case = self.pll_cases[i]
	        for j in range(4):
	            mat,solved = self.getPLLmatrix()
	            mat = self.rotPLLmatrix(mat,case)
	            for k in range(4):
	                solved = np.rot90(solved,1)
	                if all((solved == mat).reshape(9,1)):
	                    return i
	            self.U()
	    raise Exception("PLL Case not found")

	def runPLLsolver(self):
		ind = self.findPLLcase()
		for rot in self.pll_algos[ind]:
			self.rotation_dict[rot](self)
		topface = self.return2DFaces()[0]
		if len(np.unique(topface)) == 1:
			return
		else:
			raise Exception("Incorrect PLL agorithm in database")

	def runCubeSolver(self):
		self.runOLLsolver()
		self.runPLLsolver()
		for i in range(4):
			faces = [face.reshape(9,1) for face in self.return2DFaces()]
			if all([len(np.unique(face))==1 for face in faces]):
				self.compressAlgo()
				return
			self.U()
		raise Exception("Error 404!!!")