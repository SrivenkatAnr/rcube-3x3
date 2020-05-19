import numpy as np
from core.layer1_solver import layer1Solver

faces = []
for i in range(6):
    side = np.loadtxt("matrices/test-2/side{}.txt".format(i))
    faces.append(np.uint8(side))

faces = sorted(faces,key=lambda b:b[1][1],reverse=False)

face_dict = {}
side = ["top","left","front","back","right","bottom"]
for i in range(6):
    face_dict[side[i]] = faces[i]

cube = layer1Solver(face_dict)
cube.runLayer1Solver()


