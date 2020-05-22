import numpy as np
from core.cross_solver import crossSolver

class layer1Solver(crossSolver):
    def __init__(self,faces):
        super().__init__(faces)
        self.finalCorners = [ [[5,1,2],4], [[5,2,4],5], [[5,4,3],6], [[5,3,1],7] ]

    def getWhiteCorners(self):
        corners = self.cornerlist
        WhiteCorners = []
        top = []
        top_front = []
        bottom = []
        for i in range(len(corners)):
            corner = corners[i]
            if 5 in corner:
                WhiteCorners.append([corner,i])
                if i <= 3:
                    if corner.index(5):
                        top_front.append([corner,i])
                    else:
                        top.append([corner,i])
                else:
                    bottom.append([corner,i])
        crct = self.checkBottomCorners(WhiteCorners)
        return WhiteCorners,top,top_front,bottom,crct

    def checkBottomCorners(self,layer):
        crct = 0
        for corner in layer:
            if corner in self.finalCorners:
                crct += 1
        return crct

    def getCrossBack(self):
        if self.getWhiteEdges()[4] == 4:
            return
        for i in range(3):
            self.D()
            if self.getWhiteEdges()[4] == 4:
                return
        raise Exception("Cross lost")

    def rotWhiteCornerTop(self):
        #converts all the top pieces into top_front pieces
        piece = self.getWhiteCorners()[1][0]
        sort_order = {1:0, 2:1, 4:2, 3:3}
        colors = tuple(sorted(piece[0][1:], key=lambda x:sort_order[x]))
        if colors == (1,3):
            colors = (3,1)

        pos = piece[1]
        pos_dict = {0:(1,0), 1:(0,0), 2:(0,1), 3:(1,1)}
        base = np.array([[(3,1),(4,3)],[(1,2),(2,4)]])
        for i in range(4):
            self.D()
            base = np.rot90(base,1)
            ind = pos_dict[pos]
            if tuple(base[ind[0]][ind[1]]) == colors:
                break

        func_dict = {0:[lambda x:x.F(), lambda x:x.Fi()],\
                     1:[lambda x:x.L(), lambda x:x.Li()],\
                     2:[lambda x:x.B(), lambda x:x.Bi()],\
                     3:[lambda x:x.R(), lambda x:x.Ri()]}
        func = func_dict[pos]
        func[0](self)
        self.Ui()
        func[1](self)
        self.WhiteCornersTop()
        return

    def WhiteCornersTop(self):
        #slots all the top front pieces recursively
        self.getCrossBack()
        if self.getWhiteCorners()[4] == 4:
            return
        top,top_front = self.getWhiteCorners()[1:3]
        if len(top)+len(top_front) == 0:
            return 
        try:
            piece = top_front[0]
            left_flag = piece[0].index(5) - 1
            piece[0].remove(5)
        
            colors = piece[0]
            sort_order = {1:0, 2:1, 4:2, 3:3}
            colors = tuple(sorted(colors, key=lambda x:sort_order[x]))
            if colors == (1,3):
                colors = (3,1)
        
            func_dict = {(0,0):[lambda x:x.Li(), lambda x:x.L()], (0,1):[lambda x:x.F(), lambda x:x.Fi()],\
                         (1,0):[lambda x:x.Bi(), lambda x:x.B()], (1,1):[lambda x:x.L(), lambda x:x.Li()],\
                         (2,0):[lambda x:x.Ri(), lambda x:x.R()], (2,1):[lambda x:x.B(), lambda x:x.Bi()],\
                         (3,0):[lambda x:x.Fi(), lambda x:x.F()], (3,1):[lambda x:x.R(), lambda x:x.Ri()]}
            ufunc_dict = {0:[lambda x:x.Ui(), lambda x:x.U()], 1:[lambda x:x.U(), lambda x:x.Ui()]}
        
            pos = piece[1]
            pos_dict = {0:(1,0), 1:(0,0), 2:(0,1), 3:(1,1)}
            base = np.array([[(3,1),(4,3)],[(1,2),(2,4)]])
            for i in range(4):
                self.D()
                base = np.rot90(base,1)
                ind = pos_dict[pos]
                if tuple(base[ind[0]][ind[1]]) == colors:
                    break
                    
            func = func_dict[(pos,left_flag)]
            ufunc_dict[left_flag][0](self)
            func[0](self)
            ufunc_dict[left_flag][1](self)
            func[1](self)
            self.WhiteCornersTop()
            return
        except IndexError:
            self.rotWhiteCornerTop()
            return

    def WhiteCornersBottom(self):
        #pushes all wrongly slotted pieces to top layer
        if self.getWhiteCorners()[4] == 4:
            return
        wrong_pieces = [piece for piece in self.getWhiteCorners()[3] if piece not in self.finalCorners]
        pos_dict = {4:0, 5:3, 6:2, 7:1}
        func_dict = {4:[lambda x:x.F(), lambda x:x.Fi()],\
                     5:[lambda x:x.R(), lambda x:x.Ri()],\
                     6:[lambda x:x.B(), lambda x:x.Bi()],\
                     7:[lambda x:x.L(), lambda x:x.Li()]}

        for piece in wrong_pieces:
            pos = piece[1]
            for i in range(4):
                top,top_front = self.getWhiteCorners()[1:3]
                top_total = top + top_front
                if all(t[1]!=pos_dict[pos] for t in top_total):
                    break
            func_dict[pos][0](self)
            self.U()
            func_dict[pos][1](self) 
        return

    def runLayer1Solver(self):
        self.runCrossSolver()        
        while True:
            WhiteCorners,top,top_front,bottom,crct = self.getWhiteCorners()
            if crct == 4:
                break
            self.WhiteCornersTop()
            self.WhiteCornersBottom()
        self.compressAlgo()
        return