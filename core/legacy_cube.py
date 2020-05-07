import numpy as np
from .piece_3d import Piece3D
import collections

class Cube(object):
	"""Cube contains methods for rotations"""
	def __init__(self, faces):
		self.cube = np.array([Piece3D() for i in range(27)]).reshape((3, 3, 3))
		f = slice(None)
		self.slices = collections.OrderedDict([("top",(-1, slice(None), slice(None))),\
                                               ("left",(slice(None), -1, slice(None))),\
                                               ("front",(slice(None), slice(None), 0)),\
                                               ("right",(slice(None), 0, slice(None))),\
                                               ("back",(slice(None), slice(None), -1)),\
                                               ("bottom",(0, slice(None), slice(None)))])
		for face in faces.keys():
			for i in range(3):
				for j in range(3):
					self.cube[self.slices[face]][i, j].addFace(face, faces[face][i, j])
		for layer in self.cube:
			for row in layer:
				for piece in row:
					piece.fillNullFaces()

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
		if side == "top":
			#face = np.flipud(face)
			return np.rot90(face, 2)
		elif side == "bottom":
			return np.flipud(face)
		elif side == "front":
			face = np.rot90(face, 1)
			return np.fliplr(face)
		elif side == "back":
			return np.rot90(face, -1)
		elif side == "right":
			return np.rot90(face, -1)
		elif side == "left":
			face = np.rot90(face, 1)
			return np.fliplr(face)
		else:
			raise Exception("missing face")
            
	def returnAllFaces(self):
		faces = []
		for side in self.slices.keys():
			face = np.uint8(self.getFace(side))
			faces.append(face)
		return faces
