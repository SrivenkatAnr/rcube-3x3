import numpy as np
from core.layer3_solver import layer3Solver
import os
import glob

faces = []
for i in range(6):
    side = np.loadtxt("matrices/test-temp/side{}.txt".format(i))
    faces.append(np.uint8(side))

faces = sorted(faces,key=lambda b:b[1][1],reverse=False)

face_dict = {}
side = ["top","left","front","back","right","bottom"]
for i in range(6):
    face_dict[side[i]] = faces[i]

cube = layer3Solver(face_dict)
cube.runOLLsolver()

def getPieceMat(cube):
    faces = cube.return2DFaces()
    back = faces[3][0][::-1]
    left = faces[1][0]
    front = faces[2][0]
    right = faces[4][0][::-1]

    piece_mat = np.array([[ (left[0],back[0]),    (back[1]),   (back[2],right[0]) ],\
                 [ (left[1]),                     (-1),          (right[1]) ],\
                 [ (front[0],left[2]),             (front[1]),       (right[2],front[2]) ]])

    solved_mat = np.array([[ (1,3), (3), (3,4) ],\
                           [ (1),  (-1), (4) ],\
                           [ (2,1), (2), (4,2) ]])
    return piece_mat,solved_mat

def swapPieces(piece_mat,formula):
    piece_mat = piece_mat.reshape(9,1)
    new_mat = piece_mat.copy()
    for tup in formula:
        i,j = tup
        new_mat[j-1] = piece_mat[i-1]
    return new_mat.reshape(3,3)


loc = os.getcwd() + '/PLL'
pll_files = [file for file in glob.glob(loc+"**/*.npz", recursive = True)]
cases = []
algos = []
for fname in pll_files:
    data = np.load(fname)
    cases.append(data["arr_0"])
    try:
        algos.append([rot.decode('utf-8') for rot in data["arr_1"]])
    except:
        algos.append(data["arr_1"])

def findCase(cube):
    for i in range(len(cases)):
        case = cases[i]
        for j in range(4):
            mat,solved = getPieceMat(cube)
            mat = swapPieces(mat,case)
            for k in range(4):
                solved = np.rot90(solved,1)
                if all((solved == mat).reshape(9,1)):
                    print("reached crct case",i)
                    return i
            cube.U()
    raise Exception("PLL Case not found")
"""
formula = cases[20]
mat,solved = getPieceMat(cube)
for i in range(4):
    mat = getPieceMat(cube)[0]
    mat = swapPieces(mat,formula)
    for j in range(4):
        solved = np.rot90(solved,1)
        if all((solved == mat).reshape(9,1)):
            print("reached")
    print(cube.U())
"""
findCase(cube)

