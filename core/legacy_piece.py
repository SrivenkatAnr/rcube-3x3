class Piece(object):
	"""A class to store rotational info of each piece"""
	def __init__(self):
		self.colors = {}

	def addFace(self, side, color):
		self.colors[side] = color

	def fillNullFaces(self):
		for side in ("top", "bottom", "front", "back", "right", "left"):
			try:
				self.colors[side] = self.colors[side]
			except KeyError:
				self.colors[side] = 6

	def rotate(self, orientation):
		if orientation == "clockwise":
			return self.clockwise
		if orientation == "counterClockwise":
			return self.counterClockwise

	def clockwise(self, side):
		colors = self.colors

		if side == "top":
			colors["right"], colors["front"], colors["left"], colors["back"] = colors["back"], colors["right"], colors["front"], colors["left"]

		if side == "right":
			colors["top"], colors["back"], colors["bottom"], colors["front"] = colors["front"], colors["top"], colors["back"], colors["bottom"]

		if side == "front":
			colors["top"], colors["right"], colors["bottom"], colors["left"] = colors["left"], colors["top"], colors["right"], colors["bottom"]

		if side == "bottom":
			self.counterClockwise("top")

		if side == "left":
			self.counterClockwise("right")

		if side == "back":
			self.counterClockwise("front")

	def counterClockwise(self, side):
		colors = self.colors

		if side == "top":
			colors["back"], colors["right"], colors["front"], colors["left"] = colors["right"], colors["front"], colors["left"], colors["back"]

		if side == "right":
			colors["front"], colors["top"], colors["back"], colors["bottom"] = colors["top"], colors["back"], colors["bottom"], colors["front"]

		if side == "front":
			colors["left"], colors["top"], colors["right"], colors["bottom"] = colors["top"], colors["right"], colors["bottom"], colors["left"]

		if side == "bottom":
			self.clockwise("top")

		if side == "left":
			self.clockwise("right")

		if side == "back":
			self.clockwise("front")

	def colorAt(self, side):
		return self.colors[side]
		