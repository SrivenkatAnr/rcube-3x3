import numpy as np
from .legacy_piece import Piece
import OpenGL.GL as gl

class Piece3D(Piece):
	"""3d rotational information on each piece and rendering"""
	def __init__(self):
		super().__init__()
		self.vertices = np.array([[-1, 1, 1], [-1, 1, -1], [1, 1, -1], [1, 1, 1], [1, -1, 1], [1, -1, -1], [-1, -1, -1], [-1, -1, 1]])
		self.faces = {
		"top" : [0, 1, 2, 3],
		"right" : [2, 3, 4, 5],
		"bottom" : [4, 5, 6, 7],
		"left" : [6, 7, 0, 1],
		"front" : [0, 3, 4, 7],
		"back" : [1, 2, 5, 6]
		}
		self.rotationMatrix = np.eye(3)
		self.colormap = [(1,1,0),(1,0,0),(0,0,1),(0,1,0),(1,0.647,0),(1,1,1), (0,0,0)]

	def render(self, location, scale, inRotation):
		vertices = self.vertices.copy()

		if inRotation:
			vertices = (self.rotationMatrix @ vertices.transpose()).transpose()

		gl.glBegin(gl.GL_QUADS)
		for key, face in self.faces.items():
			gl.glColor3fv(self.colormap[self.colors[key]])
			for vertex in face:
				gl.glVertex3fv(scale * vertices[vertex] + location)
		gl.glEnd()

	def setRotationMatrix(self, mat):
		self.rotationMatrix = mat
