import numpy as np
from .cube_sim import Cube

class crossSolver(Cube):
	def __init__(self,faces):
		super().__init__(faces)
		self.finalEdges = [ [[5,2],8], [[5,4],9], [[5,3],10], [[5,1],11] ]

	def getWhiteEdges(self):
	    edges = self.edgelist
	    WhiteEdges = []
	    layer1 = []
	    layer2 = []
	    layer3 = []
	    for i in range(len(edges)):
	        edge = edges[i]
	        if 5 in edge:
	            WhiteEdges.append([edge,i])
	            if i>7:
	                layer1.append([edge,i])
	            elif i>3:
	                layer2.append([edge,i])
	            else:
	                layer3.append([edge,i])
	    crct = self.checkBottomEdges(WhiteEdges)
	    return WhiteEdges,layer1,layer2,layer3,crct

	def checkBottomEdges(self,layer):
	    crct = 0
	    for edge in self.finalEdges:
	        if edge in layer:
	            crct += 1
	    return crct

	def solveCrossLayer1(self):
		#rotates bottom till max crct. pushes all wrong pieces except one to top. slots that optional piece in roght position
	    for i in range(4):
	        self.D()
	        layer1 = self.getWhiteEdges()[1]
	        crct = self.getWhiteEdges()[4]
	        if len(layer1) == crct:
	            return
	    wrong_pieces = [piece for piece in layer1 if piece not in self.finalEdges]
	    p = None
	    if crct == 0:
	        for piece in wrong_pieces:
	            if piece[0][0] == 5:
	                p = piece; break
	        try:
	            wrong_pieces.remove(p)
	        except:
	            pass
	    for piece in wrong_pieces:
	        if piece[1] == 8:
	            self.F2()
	        elif piece[1] == 9:
	            self.R2()
	        elif piece[1] == 10:
	            self.B2()
	        elif piece[1] == 11:
	            self.L2()
	        else:
	            raise Exception("Piece not in layer1 wrongly included")
	    if p is not None:
	        for i in range(4):
	            self.D()
	            if self.getWhiteEdges()[4]:
	                return
	    else:
	        return

	def solveCrossLayer2(self):
		#slots all pieces in the mid layer into corresponding positions of the cross
	    index = [(0,4),(1,4),(0,5),(1,5),(0,6),(1,6),(0,7),(1,7)]
	    rotations = [lambda x:x.L(), lambda x:x.Fi(),\
	    			 lambda x:x.B(), lambda x:x.Li(),\
	    			 lambda x:x.R(), lambda x:x.Bi(),\
	    			 lambda x:x.F(), lambda x:x.Ri()]
	    positions = [(1,0), (1,1), (0,0), (1,0), (0,1), (0,0), (1,1), (0,1)]
	    rot_dict = dict(zip(index,rotations))
	    pos_dict = dict(zip(index,positions))
	    base = np.array([[3,4],[1,2]])
	    
	    layer1,layer2 = self.getWhiteEdges()[1:3]
	    try:
	        piece = layer2[0]
	    except:
	        return
	    cmd = (piece[0].index(5),piece[1])
	    piece[0].remove(5); color = piece[0][0]
	    for i in range(4):
	        self.D()
	        base = np.rot90(base,1)
	        pos = pos_dict[cmd]
	        if base[pos[0]][pos[1]] == color:
	            break
	    rot_dict[cmd](self)
	    self.solveCrossLayer1()
	    self.solveCrossLayer2()
	    return

	def solveCrossLayer3(self):
		#tries to directly slot pieces in top into the cross. if not possible, pushes them to middle layer
		layer3 = self.getWhiteEdges()[3]
		if len(layer3) == 0:
			return
		index = [0,1,2,3]
		rotations = [lambda x:x.F(), lambda x:x.L(), lambda x:x.B(), lambda x:x.R()]
		positions = [(1,1), (1,0), (0,0), (0,1)]
		rot_dict = dict(zip(index,rotations))
		pos_dict = dict(zip(index,positions))

		piece = layer3[0]
		base = np.array([[3,4],[1,2]])
		top_flag = not piece[0].index(5)
		piece[0].remove(5); color = piece[0][0]
		pos = piece[1]
		for i in range(4):
			self.D()
			base = np.rot90(base,1)
			j = pos_dict[pos]
			if base[j[0]][j[1]] == color:
				break
		rot_dict[pos](self)
		if top_flag:
			rot_dict[pos](self)
		self.solveCrossLayer1()
		self.solveCrossLayer2()
		self.solveCrossLayer3()
		return

	def runCrossSolver(self):
		while True:
		    WhiteEdges,layer1,layer2,layer3,crct = self.getWhiteEdges()
		    if crct == 4:
		        break
		    if len(layer1)>crct:
		        self.solveCrossLayer1()
		        #print("in layer1")
		    if len(layer2) > 0:
		        self.solveCrossLayer2()
		        #print("in layer3")
		    if len(layer3) > 0:
		        self.solveCrossLayer3()
		        #print("in layer2")
		        continue
		self.compressAlgo()
		return