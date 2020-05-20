import numpy as np
from core.layer2_solver import layer2Solver

faces = []
for i in range(6):
    side = np.loadtxt("matrices/test-temp/side{}.txt".format(i))
    faces.append(np.uint8(side))

faces = sorted(faces,key=lambda b:b[1][1],reverse=False)

face_dict = {}
side = ["top","left","front","back","right","bottom"]
for i in range(6):
    face_dict[side[i]] = faces[i]

cube = layer2Solver(face_dict)
print("Initial Edges: ",cube.getYellowEdges()[0])
print("Initial Corners: ",cube.getYellowCorners()[0])
cube.runLayer2Solver()
