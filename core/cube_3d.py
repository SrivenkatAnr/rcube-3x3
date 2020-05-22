import numpy as np
from .layer3_solver import layer3Solver
from .cube_sim import Cube

class Cube3D(Cube):
	"""Cube class with the 3d functions"""
	def __init__(self, faces):
		super().__init__(faces)
		self.inRotation = False
		self.rotatingSide = ""
		self.rotatingOrientation = ""
		self.positions = np.array([[[[-j, k, -i] for i in range(-1, 2)] for j in range(-1, 2)] for k in range(-1, 2)], dtype = np.float64)
		self.angle = 0
		self.rotations3D_dict = {'r':lambda x: x.rotate3D("clockwise","right"),\
								'l':lambda x: x.rotate3D("clockwise","left"),\
			 					'u':lambda x: x.rotate3D("clockwise","top"),\
			 					'f':lambda x: x.rotate3D("clockwise","front"),\
			 					'b':lambda x: x.rotate3D("clockwise","back"),\
			 					'd':lambda x: x.rotate3D("clockwise","bottom"),\
								'ri':lambda x: x.rotate3D("counterClockwise","right"),\
								'li':lambda x: x.rotate3D("counterClockwise","left"),\
								'ui':lambda x: x.rotate3D("counterClockwise","top"),\
								'fi':lambda x: x.rotate3D("counterClockwise","front"),\
								'bi':lambda x: x.rotate3D("counterClockwise","back"),\
								'di':lambda x: x.rotate3D("counterClockwise","bottom")}

	def render(self):
		positions = self.positions.copy()

		if self.inRotation:
			self.angle += 0.4 * (-1 if self.rotatingOrientation == "clockwise" else 1)
			if self.angle >= np.pi / 2 or self.angle <= -np.pi / 2:
				self.inRotation = False
				self.angle = 0
				self.rotate(self.rotatingOrientation, self.rotatingSide)

			angle = self.angle
			side = self.rotatingSide
			if side in ("bottom", "left", "back"):
				angle *= -1
			if side in ("right", "left"):
				R = np.array([[1, 0, 0], [0, np.cos(angle), -np.sin(angle)], [0, np.sin(angle), np.cos(angle)]])
			if side in ("top", "bottom"):
				R = np.array([[np.cos(angle), 0, np.sin(angle)], [0, 1, 0], [-np.sin(angle), 0, np.cos(angle)]])
			if side in ("front", "back"):
				R = np.array([[np.cos(angle), -np.sin(angle), 0], [np.sin(angle), np.cos(angle), 0], [0, 0, 1]])

			for row in self.cube[self.slices[self.rotatingSide]]:
				for piece in row:
					piece.setRotationMatrix(R)

			positions[self.slices[self.rotatingSide]] = np.array([(R @ row.transpose()).transpose() for row in positions[self.slices[self.rotatingSide]]])

		for i in range(3):
			for j in range(3):
				for k in range(3):
					self.cube[i, j, k].render(positions[i, j, k], 0.48, self.inRotation)

	def rotate3D(self, orientation, side):
		if not self.inRotation:
			self.rotatingOrientation = orientation
			self.rotatingSide = side
			self.inRotation = True

	def solve(self):
		faces = self.return2DFaces()
		faces = sorted(faces,key=lambda b:b[1][1],reverse=False)
		face_dict = {}
		side = ["top","left","front","back","right","bottom"]
		for i in range(6):
		    face_dict[side[i]] = faces[i]

		solver = layer3Solver(face_dict)
		solver.runCubeSolver()
		solver.compressAlgo()
		return solver.algo

	def printSoln(self,algo):
	    flag = True
	    if len(algo)==1:
	        flag = False
	    i=0
	    while flag:
	        for i in range(len(algo)-1):
	            if (algo[i] == algo[i+1]+'i') or (algo[i]+"i" == algo[i+1]):
	                del algo[i]; del algo[i]
	                break
	            if algo[i] == algo[i+1]:
	                del algo[i]; algo[i].replace("i",""); algo[i] += "2"
	                break
	        if (i == len(algo)-2) or (len(algo)<2):
	            flag = False
	    print("Solution found in {} moves".format(len(algo)))
	    print(*algo,sep=' ')
