import numpy as np
from .piece_3d import Piece3D
import collections

class Cube(object):
	"""Cube contains methods for rotations"""
	def __init__(self, faces):
		self.cube = np.array([Piece3D() for i in range(27)]).reshape((3, 3, 3))
		f = slice(None)
		self.slices = collections.OrderedDict([("top",(-1, f, f)),("left",(f, -1, f)),("front",(f, f, 0)),("back",(f, f, -1)),("right",(f, 0, f)),("bottom",(0, f, f))])
		for face in faces.keys():
			for i in range(3):
				for j in range(3):
					self.cube[self.slices[face]][i, j].addFace(face, faces[face][i, j])
		for layer in self.cube:
			for row in layer:
				for piece in row:
					piece.fillNullFaces()
		self.edgelist = self.returnEdges()
		self.cornerlist = self.returnCorners()

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

		return "rotated " + side + " " + orientation

	def getFace(self, side):
		face = np.array([[piece.colorAt(side) for piece in row] for row in self.cube[self.slices[side]]])
		return face
            
	def returnAllFaces(self):
		faces = []
		for side in self.slices.keys():
			face = np.uint8(self.getFace(side))
			faces.append(face)
		return faces
    
	def returnAlignedFaces(self):
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
		edgelist = []
		top_ind = [(2,1,"front"),(1,0,"left"),(0,1,"back"),(1,2,"right")]
		mid_left = ["front","left","back","right"]
		mid_right = ["left","back","right","front"]
		bottom_ind = [(0,1,"front"),(1,2,"right"),(2,1,"back"),(1,0,"left")]

		#white series clockwise, viewed from top: green to red
		for ind in top_ind:
			edgelist.append([self.cube[self.slices["top"]][ind[0]][ind[1]].colorAt("top"),\
							 self.cube[self.slices[ind[2]]][0][1].colorAt(ind[2])])
		#middle layer series clockwise, viewed from top: green-orange to red-green
		for i in range(4):
			edgelist.append([self.cube[self.slices[mid_left[i]]][1][0].colorAt(mid_left[i]),\
							 self.cube[self.slices[mid_right[i]]][1][2].colorAt(mid_right[i])])
		#yellow layer series, clockwise, viewed from bottom: green to orange
		for ind in bottom_ind:
			edgelist.append([self.cube[self.slices["bottom"]][ind[0]][ind[1]].colorAt("bottom"),\
							 self.cube[self.slices[ind[2]]][0][1].colorAt(ind[2])])
		return edgelist

	def returnCorners(self):
		cornerlist = []
		top1 = [(2,0),(0,0),(0,2),(2,2)]
		top2 = ["front","left","back","right"]
		top3 = ["left","back","right","front"]
		bot1 = [(0,0),(0,2),(2,2),(2,0)] 
		bot2 = ["left","front","right","back"]
		bot3 = ["front","right","back","left"]

		#white series clockwise, viewed from top:  green-orange to red-green
		for i in range(4):
			cornerlist.append([self.cube[self.slices["top"]][top1[i][0]][top1[i][1]].colorAt("top"),\
							   self.cube[self.slices[top2[i]]][0][0].colorAt(top2[i]),\
							   self.cube[self.slices[top3[i]]][0][2].colorAt(top3[i])])
		#white series clockwise, viewed from top:  green-orange to red-green
		for i in range(4):
			cornerlist.append([self.cube[self.slices["top"]][bot1[i][0]][bot1[i][1]].colorAt("top"),\
							   self.cube[self.slices[bot2[i]]][2][2].colorAt(bot2[i]),\
							   self.cube[self.slices[bot3[i]]][2][0].colorAt(bot3[i])])
		return cornerlist

	def checkBuild(self):
		#check if input faces are oriented properly	
		for edge in self.edgelist:
			if edge[0] + edge[1] == 5:
				return 0

		for corner in self.cornerlist:
			if (corner[0]+corner[1] == 5) or (corner[1]+corner[2] == 5) or (corner[2]+corner[0] == 5):
				return 0

		if len(set(map(tuple,self.edgelist))) != len(self.edgelist):
			return 0

		if len(set(map(tuple,self.cornerlist))) != len(self.cornerlist):
			return 0

		return 5


