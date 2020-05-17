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


