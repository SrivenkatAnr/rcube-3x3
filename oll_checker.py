import numpy as np
import os
import glob
from core.cube_sim import Cube
from core.layer2_solver import layer2Solver

loc = os.getcwd() + "/OLL"
print(loc)

oll_files = [file for file in glob.glob(loc+"**/*.npz", recursive = True)]

case = []
algo = []
for fname in oll_files:
    data = np.load(fname)
    case.append(data["arr_0"])
    try:
    	algo.append([rot.decode('utf-8') for rot in data["arr_1"]])
    except:
    	algo.append(data["arr_1"])

faces = []
for i in range(6):
    side = np.loadtxt("matrices/solved/side{}.txt".format(i))
    faces.append(np.uint8(side))

faces = sorted(faces,key=lambda b:b[1][1],reverse=False)

face_dict = {}
side = ["top","left","front","back","right","bottom"]
for i in range(6):
    face_dict[side[i]] = faces[i]

for i in range(len(algo)):
	print(i)
	cube = Cube(face_dict)
	alg = algo[i]
	for rot in alg:
		cube.rotation_dict[rot](cube)

	nfaces = cube.return2DFaces()
	nfaces = sorted(nfaces,key=lambda b:b[1][1],reverse=False)
	nface_dict = {}
	nside = ["top","left","front","back","right","bottom"]
	for j in range(6):
		nface_dict[nside[j]] = nfaces[j]

	solver = layer2Solver(nface_dict)
	solver.runLayer2Solver()
	if len(solver.algo) == 0:
		print("done",i)
	else:
		print("exception",i)
"""
cube = Cube(face_dict)
for rot in algo[43]:
	cube.rotation_dict[rot](cube)

sides = cube.return2DFaces()
i=0
for side in sides:
	np.savetxt("matrices/test-temp/side{}.txt".format(i),side)
	i+=1

print(algo[43])
print(oll_files[43])
"""