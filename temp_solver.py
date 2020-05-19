import numpy as np
from core.layer1_solver import layer1Solver

faces = []
for i in range(6):
    side = np.loadtxt("matrices/test-5/side{}.txt".format(i))
    faces.append(np.uint8(side))

faces = sorted(faces,key=lambda b:b[1][1],reverse=False)

face_dict = {}
side = ["top","left","front","back","right","bottom"]
for i in range(6):
    face_dict[side[i]] = faces[i]

cube = layer1Solver(face_dict)
cube.runLayer1Solver()

finalMiddle = [ [[2,1],4], [[1,3],5], [[3,4],6], [[4,2],7] ]

def getMidEdges(cube):
    edges = cube.edgelist
    middle = []
    top = []
    for i in range(len(edges)):
        edge = edges[i]
        if (5 not in edge) and (0 not in edge):
            if i>3:
                middle.append([edge,i])
            else:
                top.append([edge,i])
    crct = checkMidLayer(middle)
    return middle,top,crct

def checkMidLayer(layer):
    crct = 0
    for piece in layer:
        if piece in finalMiddle:
            crct += 1
    return crct

print(getMidEdges(cube))

def slotMidEdges(cube,color):
    #print("entered slot func")
    color_dict = {0:2, 1:1, 2:3, 3:4}
    func_dict = {(3,4):[lambda x: x.B(), lambda x: x.Bi()], (4,3):[lambda x: x.Ri(), lambda x: x.R()],\
                 (4,2):[lambda x: x.R(), lambda x: x.Ri()], (2,4):[lambda x: x.Fi(), lambda x: x.F()],\
                 (2,1):[lambda x: x.F(), lambda x: x.Fi()], (1,2):[lambda x: x.Li(), lambda x: x.L()],\
                 (1,3):[lambda x: x.L(), lambda x: x.Li()], (3,1):[lambda x: x.Bi(), lambda x: x.B()]}
    try:
        top = getMidEdges(cube)[1]
        if color is None:
            color = top[0][0]
        
        edge = [piece for piece in top if piece[0] == color]
        edge = edge[0]
        if color[1] != color_dict[edge[1]]:
            cube.U()
            slotMidEdges(cube,color)
            return
        else:
            print(color)
            if color in [[3,4],[4,2],[2,1],[1,3]]:
                up = [lambda x: x.U(), lambda x: x.Ui()]
            else:
                up = [lambda x: x.Ui(), lambda x: x.U()]
            func = func_dict[tuple(color)]
            up[0](cube)
            func[0](cube)
            up[1](cube)
            func[1](cube)
            cube.runLayer1Solver()
            #print("piece slotted",getMidEdges(cube)[1])
        slotMidEdges(cube,None)
        return
    except:
        print("quitting",getMidEdges(cube)[2])
        return


def pushMidEdges(cube):
    edges = [edge for edge in getMidEdges(cube)[0] if edge not in finalMiddle]
    func_dict = {4:[lambda x: x.Li(), lambda x: x.L()],\
                 5:[lambda x: x.Bi(), lambda x: x.B()],\
                 6:[lambda x: x.Ri(), lambda x: x.R()],\
                 7:[lambda x: x.Fi(), lambda x: x.F()]}
    for edge in edges:
        pos = edge[1]
        func = func_dict[pos]
        func[0](cube)
        cube.U()
        func[1](cube)
    return

while True:
    crct = getMidEdges(cube)[-1]
    if crct==4:
        break
    slotMidEdges(cube,None)
    pushMidEdges(cube)
