import numpy as np
from .piece_3d import Piece3D
import collections

class CubeClass(object):
	"""Cube contains methods for rotations"""
	def __init__(self, faces):
		self.cube = np.array([Piece3D() for i in range(27)]).reshape((3, 3, 3))
		f = slice(None)
		self.slices = collections.OrderedDict([("top",(-1, f, f)),("left",(f, -1, f)),("front",(f, f, 0)),("back",(f, f, -1)),("right",(f, 0, f)),("bottom",(0, f, f))])
		faces = self.processInputFaces(faces)
		self.setFaces(faces)

	def setFaces(self,faces):
		i = 0
		keys = list(faces.keys())
		for l0 in range(4):
			for l1 in range(4):
				for l2 in range(4):
					for l3 in range(4):
						for l4 in range(4):
							for l5 in range(4):
								faces[keys[5]] = np.rot90(faces[keys[5]],1)
								i += 1
								if self.updateCube(faces):
									return 1
							faces[keys[4]] = np.rot90(faces[keys[4]],1)
						faces[keys[3]] = np.rot90(faces[keys[3]],1)
					faces[keys[2]] = np.rot90(faces[keys[2]],1)
				faces[keys[1]] = np.rot90(faces[keys[1]],1)
			faces[keys[0]] = np.rot90(faces[keys[0]],1)
		raise Exception("Invalid face input")	

	def updateCube(self,faces):
		for key in faces.keys():
			for i in range(3):
				for j in range(3):
					self.cube[self.slices[key]][i, j].addFace(key, faces[key][i, j])
		for layer in self.cube:
			for row in layer:
				for piece in row:
					piece.fillNullFaces()

		self.edgelist = self.returnEdges()
		self.cornerlist = self.returnCorners()
		return self.checkBuild()

	def rotate(self, orientation, side):
		cube = self.cube
		if orientation not in ("clockwise", "counterClockwise"):
			raise Exception("orientation can either be clockwise or counterClockwise")

		rotateDir = (orientation == "clockwise")
		if side in ("bottom", "left", "front"):
			rotateDir = not rotateDir

		cube[self.slices[side]] = np.rot90(cube[self.slices[side]], 1 if rotateDir else -1)
		try:
			for row in cube[self.slices[side]]:
				for piece in row:
					piece.rotate(orientation)(side)
		except KeyError:
			pass
		self.edgelist = self.returnEdges()
		self.cornerlist = self.returnCorners()
		return "rotated " + side + " " + orientation

	def getFace(self, side):
		face = np.array([[piece.colorAt(side) for piece in row] for row in self.cube[self.slices[side]]])
		return face
 
	def processInputFaces(self,faces):
		for key in faces.keys():
			if key == "top":
				temp = np.flipud(faces[key])
				faces[key] = np.rot90(temp,1)
			elif key == "bottom":
				faces[key] = np.rot90(faces[key],1)
			elif key == "front":
				faces[key] = np.rot90(faces[key],2)
			elif key == "back":
				faces[key] = np.flipud(faces[key])
			elif key == "right":
				faces[key] = np.flipud(faces[key])
			elif key == "left":
				faces[key] = np.rot90(faces[key],2)
		return faces

	def return2DFaces(self):
		faces = []
		for side in self.slices.keys():
			temp = self.getFace(side)
			if side == "top":
				temp = np.rot90(temp, -1)
				temp = np.flipud(temp)
			elif side == "bottom":
				temp =  np.rot90(temp,-1)
			elif side == "front":
				temp = np.rot90(temp, 2)
			elif side == "back":
				temp = np.flipud(temp)
			elif side == "right":
				temp = np.flipud(temp)
			elif side == "left":
				temp = np.rot90(temp, 2)
			faces.append(temp)
		return faces
    
	def return3DFaces(self):
		faces = []
		for side in self.slices.keys():
			temp = self.getFace(side)
			if side == "top":
				temp = np.rot90(temp, 2)
			elif side == "bottom":
				temp =  np.flipud(temp)
			elif side == "front":
				temp = np.rot90(temp, 1)
				temp = np.fliplr(temp)
			elif side == "back":
				temp = np.rot90(temp, -1)
			elif side == "right":
				temp = np.rot90(temp, -1)
			elif side == "left":
				temp = np.rot90(temp, 1)
				temp = np.fliplr(temp)
			faces.append(temp)
		return faces

	def returnEdges(self):
		mat = self.return2DFaces()		
		edgelist = []
		top_ind = [(2,1,2),(1,0,1),(0,1,3),(1,2,4)]
		mid_ind = [(2,1),(1,3),(3,4),(4,2)]
		bottom_ind = [(0,1,2),(1,2,4),(2,1,3),(1,0,1)]

		#white series clockwise, viewed from top: green to red
		for ind in top_ind:
			edgelist.append([ mat[0][ind[0]][ind[1]], mat[ind[2]][0][1] ])
		#middle layer series clockwise, viewed from top: green-orange to red-green
		for ind in mid_ind:
			edgelist.append([ mat[ind[0]][1][0], mat[ind[1]][1][2] ])
		#yellow layer series, clockwise, viewed from bottom: green to orange
		for ind in bottom_ind:
			edgelist.append([ mat[5][ind[0]][ind[1]], mat[ind[2]][2][1] ])
		return edgelist

	def returnCorners(self):
		mat = self.return2DFaces()
		cornerlist = []
		top_ind = [(2,0,2,1),(0,0,1,3),(0,2,3,4),(2,2,4,2)]
		bot_ind = [(0,0,1,2),(0,2,2,4),(2,2,4,3),(2,0,3,1)] 

		#white series clockwise, viewed from top:  green-orange to red-green
		for ind in top_ind:
			cornerlist.append([ mat[0][ind[0]][ind[1]], mat[ind[2]][0][0], mat[ind[3]][0][2] ])
		#yellow series clockwise, viewed from bottom:  orange-green to blue-orange
		for ind in bot_ind:
			cornerlist.append([ mat[5][ind[0]][ind[1]], mat[ind[2]][2][2], mat[ind[3]][2][0] ])
		return cornerlist

	def checkBuild(self):
		#check if input faces are oriented properly	
		for edge in self.edgelist:
			if (edge[0] + edge[1] == 5) or edge[0] == edge[1]:
				return False
		for corner in self.cornerlist:
			if (corner[0]+corner[1] == 5) or (corner[1]+corner[2] == 5) or (corner[2]+corner[0] == 5) or (corner[0] == corner[1]) or (corner[1] == corner[2]) or (corner[2] == corner[0]):
				return False
				
		if len(set(map(tuple,self.edgelist))) != len(self.edgelist):
			return False
		if len(set(map(tuple,self.cornerlist))) != len(self.cornerlist):
			return False

		return True


