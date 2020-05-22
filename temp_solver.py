import numpy as np
from core.layer3_solver import layer3Solver
import os
import glob
"""
loc = os.getcwd() + "/OLL"

oll_files = [file for file in glob.glob(loc+"**/*.npz", recursive = True)]

cases = []
algos = []
for fname in oll_files:
    data = np.load(fname)
    cases.append(data["arr_0"])
    try:
    	algos.append([rot.decode('utf-8') for rot in data["arr_1"]])
    except:
    	algos.append(data["arr_1"])
"""
faces = []
for i in range(6):
    side = np.loadtxt("matrices/test-temp/side{}.txt".format(i))
    faces.append(np.uint8(side))

faces = sorted(faces,key=lambda b:b[1][1],reverse=False)

face_dict = {}
side = ["top","left","front","back","right","bottom"]
for i in range(6):
    face_dict[side[i]] = faces[i]
"""
cube = layer2Solver(face_dict)
cube.runLayer2Solver()
def findMat(cube):
    nfaces = cube.return2DFaces()
    nfaces = sorted(nfaces,key=lambda x:x[1][1], reverse = False)

    cmat = np.ones((5,5))
    cmat[1:-1,1:-1] = nfaces[0]
    cmat[1:-1,0] = nfaces[1][0,:]
    cmat[1:-1,4] = nfaces[4][0,:][::-1]
    cmat[0,1:-1] = nfaces[3][0,:][::-1]
    cmat[4,1:-1] = nfaces[2][0,:]
    
    nmat = [[1 if col==0 else 0 for col in row] for row in cmat]
    nmat[0][0] = 0; nmat[0][4] = 0; nmat[4][0] = 0; nmat[4][4] = 0
    return nmat,cmat

def findCase(cube):
    for i in range(4):
        mat = findMat(cube)[0]
        for i in range(len(cases)):
            case = cases[i]
            if all((case == mat).reshape(25,1)):
                return case,algos[i]
        cube.U()
    raise Exception("Case not found")

algo = findCase(cube)[1]
for rot in algo:
    cube.rotation_dict[rot](cube)

print(cube.return2DFaces()[0])
"""
cube = layer3Solver(face_dict)
cube.runOLLsolver()