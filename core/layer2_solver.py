import numpy as np
from core.layer1_solver import layer1Solver

class layer2Solver(layer1Solver):
    def __init__(self,faces):
        super().__init__(faces)
        self.finalMiddle = [ [[2,1],4], [[1,3],5], [[3,4],6], [[4,2],7] ]

    def getMidEdges(self):
        edges = self.edgelist
        middle = []
        top = []
        for i in range(len(edges)):
            edge = edges[i]
            if (5 not in edge) and (0 not in edge):
                if i>3:
                    middle.append([edge,i])
                else:
                    top.append([edge,i])
        crct = self.checkMidLayer(middle)
        return middle,top,crct

    def checkMidLayer(self,layer):
        crct = 0
        for piece in layer:
            if piece in self.finalMiddle:
                crct += 1
        return crct

    def slotMidEdges(self,color):
        #print("entered slot func")
        color_dict = {0:2, 1:1, 2:3, 3:4}
        func_dict = {(3,4):[lambda x: x.B(), lambda x: x.Bi()], (4,3):[lambda x: x.Ri(), lambda x: x.R()],\
                     (4,2):[lambda x: x.R(), lambda x: x.Ri()], (2,4):[lambda x: x.Fi(), lambda x: x.F()],\
                     (2,1):[lambda x: x.F(), lambda x: x.Fi()], (1,2):[lambda x: x.Li(), lambda x: x.L()],\
                     (1,3):[lambda x: x.L(), lambda x: x.Li()], (3,1):[lambda x: x.Bi(), lambda x: x.B()]}
        try:
            top = self.getMidEdges()[1]
            if color is None:
                color = top[0][0]
            
            edge = [piece for piece in top if piece[0] == color]
            edge = edge[0] 
            if color[1] != color_dict[edge[1]]:
                self.U()
                self.slotMidEdges(color)
                return
            else:
                #print(color)
                if color in [[3,4],[4,2],[2,1],[1,3]]:
                    up = [lambda x: x.U(), lambda x: x.Ui()]
                else:
                    up = [lambda x: x.Ui(), lambda x: x.U()]
                func = func_dict[tuple(color)]
                up[0](self)
                func[0](self)
                up[1](self)
                func[1](self)
                self.runLayer1Solver()
                #print("piece slotted",getMidEdges(cube)[1])
            self.slotMidEdges(None)
            return
        except:
            #print("quitting",self.getMidEdges()[2])
            return

    def pushMidEdges(self):
        edges = [edge for edge in self.getMidEdges()[0] if edge not in self.finalMiddle]
        func_dict = {4:[lambda x: x.Li(), lambda x: x.L()],\
                     5:[lambda x: x.Bi(), lambda x: x.B()],\
                     6:[lambda x: x.Ri(), lambda x: x.R()],\
                     7:[lambda x: x.Fi(), lambda x: x.F()]}
        for edge in edges:
            pos = edge[1]
            func = func_dict[pos]
            func[0](self)
            self.U()
            func[1](self)
        return

    def runLayer2Solver(self):
        self.runLayer1Solver()
        while True:
            crct = self.getMidEdges()[-1]
            if crct==4:
                break
            self.slotMidEdges(None)
            self.pushMidEdges()
        self.compressAlgo()
        return
