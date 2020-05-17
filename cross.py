import numpy as np
from core.legacy_cube import Cube

def R(cube):
    cube.rotate("clockwise","right")
def Ri(cube):
    cube.rotate("counterClockwise","right")
def R2(cube):
    cube.rotate("clockwise","right")
    cube.rotate("clockwise","right")
def L(cube):
    cube.rotate("clockwise","left")
def Li(cube):
    cube.rotate("counterClockwise","left")
def L2(cube):
    cube.rotate("clockwise","left")
    cube.rotate("clockwise","left")
def F(cube):
    cube.rotate("clockwise","front")
def Fi(cube):
    cube.rotate("counterClockwise","front")
def F2(cube):
    cube.rotate("clockwise","front")
    cube.rotate("clockwise","front")
def B(cube):
    cube.rotate("clockwise","back")
def Bi(cube):
    cube.rotate("counterClockwise","back")
def B2(cube):
    cube.rotate("clockwise","back")
    cube.rotate("clockwise","back")
def U(cube):
    cube.rotate("clockwise","top")
def Ui(cube):
    cube.rotate("counterClockwise","top")
def U2(cube):
    cube.rotate("clockwise","top")
    cube.rotate("clockwise","top")
def D(cube):
    cube.rotate("clockwise","bottom")
def Di(cube):
    cube.rotate("counterClockwise","bottom")
def D2(cube):
    cube.rotate("clockwise","bottom")
    cube.rotate("clockwise","bottom")

faces = []
for i in range(6):
    side = np.loadtxt("matrices/test-temp/side{}.txt".format(i))
    faces.append(np.uint8(side))

faces = sorted(faces,key=lambda b:b[1][1],reverse=False)

face_dict = {}
side = ["top","left","front","back","right","bottom"]
for i in range(6):
    face_dict[side[i]] = faces[i]

finalBottom = [ [[5,2],8], [[5,4],9], [[5,3],10], [[5,1],11] ]

def getYellowEdges(cube):
    edges = cube.edgelist
    yellow = []
    layer1 = []
    layer2 = []
    layer3 = []
    for i in range(len(edges)):
        edge = edges[i]
        if 5 in edge:
            yellow.append([edge,i])
            if i>7:
                layer1.append([edge,i])
            elif i>3:
                layer2.append([edge,i])
            else:
                layer3.append([edge,i])
    crct = checkBottom(yellow)
    return yellow,layer1,layer2,layer3,crct

cube = Cube(face_dict)

#crct: no. of crct pieces in crct ori
def checkBottom(layer1):
    crct = 0
    for edge in finalBottom:
        if edge in layer1:
            crct += 1
    return crct

def yellowInLayer1(cube):
    for i in range(4):
        D(cube)
        layer1 = getYellowEdges(cube)[1]
        crct = getYellowEdges(cube)[4]
        if len(layer1) == crct:
            return
    wrong_pieces = [piece for piece in layer1 if piece not in finalBottom]
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
        #print("moved")
        if piece[1] == 8:
            F(cube); F(cube);
        elif piece[1] == 9:
            R(cube); R(cube)
        elif piece[1] == 10:
            B(cube); B(cube)
        elif piece[1] == 11:
            L(cube); L(cube)
        else:
            raise Exception("Piece not in layer1 wrongly included")
    if p is not None:
        for i in range(4):
            D(cube)
            if getYellowEdges(cube)[4]:
                return
    else:
        return


def yellowInLayer2(cube):
   # print("entered 2")
    rot_dict = {(0,4):lambda x:L(x), (1,4):lambda x:Fi(x),\
                (0,5):lambda x:B(x), (1,5):lambda x:Li(x),\
                (0,6):lambda x:R(x), (1,6):lambda x:Bi(x),\
                (0,7):lambda x:F(x), (1,7):lambda x:Ri(x)}
    pos_dict = {(0,4):(1,0), (1,4):(1,1),\
                (0,5):(0,0), (1,5):(1,0),\
                (0,6):(0,1), (1,6):(0,0),\
                (0,7):(1,1), (1,7):(0,1)}
    base = np.array([[3,4],[1,2]])
    
    layer1,layer2 = getYellowEdges(cube)[1:3]
    try:
        piece = layer2[0]
    except:
        #print("done with layer2",len(layer2))
        return
    cmd = (piece[0].index(5),piece[1])
    piece[0].remove(5); color = piece[0][0]
    for i in range(4):
        D(cube)
        base = np.rot90(base,1)
        ij = pos_dict[cmd]
        if base[ij[0]][ij[1]] == color:
            break
    rot_dict[cmd](cube)
    #print("moved in 2")
    yellowInLayer1(cube)
    #print("returned from 1")
    #print(getYellowEdges(cube)[4])
    yellowInLayer2(cube)


def yellowInLayer3(cube):
    #print("entered 3")
    layer3 = getYellowEdges(cube)[3]
    if len(layer3) == 0:
        #print("done with layer3",len(layer3))
        return
    rot_dict = {0:lambda x:F(x),\
                1:lambda x:L(x),\
                2:lambda x:B(x),\
                3:lambda x:R(x)}
    pos_dict = {0:(1,1), 1:(1,0), 2:(0,0), 3:(0,1)}
    piece = layer3[0]
    base = np.array([[3,4],[1,2]])
    top_flag = not piece[0].index(5)
    piece[0].remove(5); color = piece[0][0]
    pos = piece[1]
    for i in range(4):
        D(cube)
        base = np.rot90(base,1)
        j = pos_dict[pos]
        if base[j[0]][j[1]] == color:
            break
    rot_dict[pos](cube)
    #print("moved in 3",i)
    if top_flag:
        rot_dict[pos](cube)
    yellowInLayer1(cube)
    yellowInLayer2(cube)
    #print(getYellowEdges(cube)[0])
    yellowInLayer3(cube)

print(getYellowEdges(cube)[0])

while True:
    yellow,layer1,layer2,layer3,crct = getYellowEdges(cube)
    if crct == 4:
        print(yellow)
        break
    if len(layer1)>crct:
        yellowInLayer1(cube)
        #yellow,layer1,layer2,layer3,crct = getYellowEdges(cube)
        #print("in layer1")
    if len(layer2) > 0:
        yellowInLayer2(cube)
        #yellow,layer1,layer2,layer3,crct = getYellowEdges(cube)
        #print("in layer3")
    if len(layer3) > 0:
        yellowInLayer3(cube)
        #yellow,layer1,layer2,layer3,crct = getYellowEdges(cube)
        #print("in layer2")
        continue
