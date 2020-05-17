from .legacy_cube import Cube

class CubeSim(Cube):
	def __init__(self,faces):
		super().__init__(faces)
		pass

	def R(self):
		self.rotate("clockwise","right")

	def Ri(self):
		self.rotate("counterClockwise","right")

	def R2(self):
		self.rotate("clockwise","right")
		self.rotate("clockwise","right")

	def L(self):
		self.rotate("clockwise","left")

	def Li(self):
		self.rotate("counterClockwise","left")

	def L2(self):
		self.rotate("clockwise","left")	
		self.rotate("clockwise","left")

	def F(self):
		self.rotate("clockwise","front")

	def Fi(self):
		self.rotate("counterClockwise","front")

	def F2(self):
		self.rotate("clockwise","front")
		self.rotate("clockwise","front")

	def B(self):
		self.rotate("clockwise","back")

	def Bi(self):
		self.rotate("counterClockwise","back")

	def B2(self):
		self.rotate("clockwise","back")
		self.rotate("clockwise","back")

	def U(self):
		self.rotate("clockwise","top")

	def Ui(self):
		self.rotate("counterClockwise","top")

	def U2(self):
		self.rotate("clockwise","top")
		self.rotate("clockwise","top")

	def D(self):
		self.rotate("clockwise","bottom")

	def Di(self):
		self.rotate("counterClockwise","bottom")

	def D2(self):
		self.rotate("clockwise","bottom")
		self.rotate("clockwise","bottom")
