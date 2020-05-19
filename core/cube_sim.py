from .legacy_cube import CubeClass

class Cube(CubeClass):
	def __init__(self,faces):
		super().__init__(faces)
		self.algo = []
		self.rotation_dict = {'r':lambda x:x.R(),\
			 				 'l':lambda x:x.L(),\
			 				 'u':lambda x:x.U(),\
			 				 'f':lambda x:x.F(),\
			 				 'b':lambda x:x.B(),\
			 				 'd':lambda x:x.D(),\
			 				 'ri':lambda x:x.Ri(),\
			 				 'li':lambda x:x.Li(),\
			 				 'ui':lambda x:x.Ui(),\
			 				 'fi':lambda x:x.Fi(),\
			 				 'bi':lambda x:x.Bi(),\
			 				 'di':lambda x:x.Di()}

	def R(self):
		self.rotate("clockwise","right")
		self.algo.append('r')
		return 'R'

	def Ri(self):
		self.rotate("counterClockwise","right")
		self.algo.append('ri')
		return 'Ri'

	def R2(self):
		self.rotate("clockwise","right")
		self.rotate("clockwise","right")
		self.algo.append('r')
		self.algo.append('r')
		return 'R2'

	def L(self):
		self.rotate("clockwise","left")
		self.algo.append('l')
		return 'L'

	def Li(self):
		self.rotate("counterClockwise","left")
		self.algo.append('li')
		return 'Li'

	def L2(self):
		self.rotate("clockwise","left")	
		self.rotate("clockwise","left")
		self.algo.append('l')
		self.algo.append('l')
		return 'L2'

	def F(self):
		self.rotate("clockwise","front")
		self.algo.append('f')
		return 'F'

	def Fi(self):
		self.rotate("counterClockwise","front")
		self.algo.append('fi')
		return 'Fi'

	def F2(self):
		self.rotate("clockwise","front")
		self.rotate("clockwise","front")
		self.algo.append('f')
		self.algo.append('f')
		return 'F2'

	def B(self):
		self.rotate("clockwise","back")
		self.algo.append('b')
		return 'B'

	def Bi(self):
		self.rotate("counterClockwise","back")
		self.algo.append('bi')
		return 'Bi'

	def B2(self):
		self.rotate("clockwise","back")
		self.rotate("clockwise","back")
		self.algo.append('b')
		self.algo.append('b')
		return 'B2'

	def U(self):
		self.rotate("clockwise","top")
		self.algo.append('u')
		return 'U'

	def Ui(self):
		self.rotate("counterClockwise","top")
		self.algo.append('ui')
		return 'Ui'

	def U2(self):
		self.rotate("clockwise","top")
		self.rotate("clockwise","top")
		self.algo.append('u')
		self.algo.append('u')
		return 'U2'

	def D(self):
		self.rotate("clockwise","bottom")
		self.algo.append('d')
		return 'D'

	def Di(self):
		self.rotate("counterClockwise","bottom")
		self.algo.append('di')
		return 'Di'

	def D2(self):
		self.rotate("clockwise","bottom")
		self.rotate("clockwise","bottom")
		self.algo.append('d')
		self.algo.append('d')
		return 'D2'

	def compressAlgo(self):
		algo = self.algo

