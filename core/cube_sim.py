from .legacy_cube import CubeClass

class Cube(CubeClass):
	def __init__(self,faces):
		super().__init__(faces)
		pass

	def R(self):
		self.rotate("clockwise","right")
		return 'R'

	def Ri(self):
		self.rotate("counterClockwise","right")
		return 'Ri'

	def R2(self):
		self.rotate("clockwise","right")
		self.rotate("clockwise","right")
		return 'R2'

	def L(self):
		self.rotate("clockwise","left")
		return 'L'

	def Li(self):
		self.rotate("counterClockwise","left")
		return 'Li'

	def L2(self):
		self.rotate("clockwise","left")	
		self.rotate("clockwise","left")
		return 'L2'

	def F(self):
		self.rotate("clockwise","front")
		return 'F'

	def Fi(self):
		self.rotate("counterClockwise","front")
		return 'Fi'

	def F2(self):
		self.rotate("clockwise","front")
		self.rotate("clockwise","front")
		return 'F2'

	def B(self):
		self.rotate("clockwise","back")
		return 'B'

	def Bi(self):
		self.rotate("counterClockwise","back")
		return 'Bi'

	def B2(self):
		self.rotate("clockwise","back")
		self.rotate("clockwise","back")
		return 'B2'

	def U(self):
		self.rotate("clockwise","top")
		return 'U'

	def Ui(self):
		self.rotate("counterClockwise","top")
		return 'Ui'

	def U2(self):
		self.rotate("clockwise","top")
		self.rotate("clockwise","top")
		return 'U2'

	def D(self):
		self.rotate("clockwise","bottom")
		return 'D'

	def Di(self):
		self.rotate("counterClockwise","bottom")
		return 'Di'

	def D2(self):
		self.rotate("clockwise","bottom")
		self.rotate("clockwise","bottom")
		return 'D2'
