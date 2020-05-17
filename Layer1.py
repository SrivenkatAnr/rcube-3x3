import numpy as np
from core.cross_solve import cubeCross

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
print(cube.getCrossEdges()[0])
cube.runCrossSolver()