import numpy as np
from core.cross_solver import cubeCross

faces = []
for i in range(6):
    side = np.loadtxt("matrices/test-temp/side{}.txt".format(i))
    faces.append(np.uint8(side))

faces = sorted(faces,key=lambda b:b[1][1],reverse=False)

face_dict = {}
side = ["top","left","front","back","right","bottom"]
for i in range(6):
    face_dict[side[i]] = faces[i]

cube = cubeCross(face_dict)
cube.runCrossSolver()

finalCorners = [ [[5,1,2],4], [[5,2,4],5], [[5,4,3],6], [[5,3,1],7] ]

#assuming that cross is solved
def getYellowCorners(cube):
    corners = cube.cornerlist
    yellow = []
    top = []
    top_front = []
    bottom = []
    for i in range(len(corners)):
        corner = corners[i]
        if 5 in corner:
            yellow.append([corner,i])
            if i <= 3:
                if corner.index(5):
                    top_front.append([corner,i])
                else:
                    top.append([corner,i])
            else:
                bottom.append([corner,i])
    crct = checkBottom(yellow)
    return yellow,top,top_front,bottom,crct

def checkBottom(yellow):
    crct = 0
    for corner in yellow:
        if corner in finalCorners:
            crct += 1
    return crct

def getCrossBack(cube):
    if cube.getCrossEdges()[4] == 4:
        return
    for i in range(3):
        cube.D()
        if cube.getCrossEdges()[4] == 4:
            return
    raise Exception("Cross lost")

def rotateTopCorner(cube):
    #converts all the top pieces into top_front pieces
    piece = getYellowCorners(cube)[1][0]
    sort_order = {1:0, 2:1, 4:2, 3:3}
    colors = tuple(sorted(piece[0][1:], key=lambda x:sort_order[x]))
    if colors == (1,3):
        colors = (3,1)

    pos = piece[1]
    pos_dict = {0:(1,0), 1:(0,0), 2:(0,1), 3:(1,1)}
    base = np.array([[(3,1),(4,3)],[(1,2),(2,4)]])
    for i in range(4):
        cube.D()
        base = np.rot90(base,1)
        ind = pos_dict[pos]
        if tuple(base[ind[0]][ind[1]]) == colors:
            break

    func_dict = {0:[lambda x:x.F(), lambda x:x.Fi()],\
                 1:[lambda x:x.L(), lambda x:x.Li()],\
                 2:[lambda x:x.B(), lambda x:x.Bi()],\
                 3:[lambda x:x.R(), lambda x:x.Ri()]}
    func = func_dict[pos]
    func[0](cube)
    cube.Ui()
    func[1](cube)
    solveTopLayer(cube)

def solveTopLayer(cube):
    #slots all the top front pieces recursively
    print("in solve top")
    getCrossBack(cube)
    if getYellowCorners(cube)[4] == 4:
        return
    top,top_front = getYellowCorners(cube)[1:3]
    if len(top)+len(top_front) == 0:
        return 
    try:
        piece = top_front[0]
        print(len(top),len(top_front),getYellowCorners(cube)[4])
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
            cube.D()
            base = np.rot90(base,1)
            ind = pos_dict[pos]
            if tuple(base[ind[0]][ind[1]]) == colors:
                break
                
        func = func_dict[(pos,left_flag)]
        ufunc_dict[left_flag][0](cube)
        func[0](cube)
        ufunc_dict[left_flag][1](cube)
        func[1](cube)
        solveTopLayer(cube)

    except IndexError:
        print("entering rot")
        rotateTopCorner(cube)


def solveBotLayer(cube):
    #pushes all wrongly slotted pieces to top layer
    print("in solve bot")
    if getYellowCorners(cube)[4] == 4:
        return
    wrong_pieces = [piece for piece in getYellowCorners(cube)[3] if piece not in finalCorners]
    pos_dict = {4:0, 5:3, 6:2, 7:1}
    func_dict = {4:[lambda x:x.F(), lambda x:x.Fi()],\
                 5:[lambda x:x.R(), lambda x:x.Ri()],\
                 6:[lambda x:x.B(), lambda x:x.Bi()],\
                 7:[lambda x:x.L(), lambda x:x.Li()]}

    for piece in wrong_pieces:
        pos = piece[1]
        for i in range(4):
            top,top_front = getYellowCorners(cube)[1:3]
            top_total = top + top_front
            if all(t[1]!=pos_dict[pos] for t in top_total):
                break
        func_dict[pos][0](cube)
        cube.U()
        func_dict[pos][1](cube) 

    return

while True:
    if getYellowCorners(cube)[4] == 4:
        break
    solveTopLayer(cube)
    solveBotLayer(cube)

print(getYellowCorners(cube))



