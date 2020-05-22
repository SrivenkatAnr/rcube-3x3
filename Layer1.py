import numpy as np
from core.layer3_solver import layer3Solver

faces = []
for i in range(6):
    side = np.loadtxt("matrices/scrambled-3/side{}.txt".format(i))
    faces.append(np.uint8(side))

faces = sorted(faces,key=lambda b:b[1][1],reverse=False)

face_dict = {}
side = ["top","left","front","back","right","bottom"]
for i in range(6):
    face_dict[side[i]] = faces[i]

cube = layer3Solver(face_dict)
print("Initial Edges: ",cube.getYellowEdges()[0])
print("Initial Corners: ",cube.getYellowCorners()[0])
cube.runCubeSolver()
cube.compressAlgo()

def printSoln(algo):
    flag = True
    if len(algo)==1:
        flag = False
    while flag:
        for i in range(len(algo)-1):
            if (algo[i] == algo[i+1]+'i') or (algo[i]+"i" == algo[i+1]):
                del algo[i]; del algo[i]
                break
            if algo[i] == algo[i+1]:
                del algo[i]; algo[i].replace("i",""); algo[i] += "2"
                break
        if (i == len(algo)-2) or (len(algo)<3):
            flag = False
    print(*algo,sep=',')

printSoln(cube.algo)