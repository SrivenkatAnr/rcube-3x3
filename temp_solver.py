import numpy as np
from core.cube_sim import Cube

faces = []
for i in range(6):
    side = np.loadtxt("matrices/test-temp/side{}.txt".format(i))
    faces.append(np.uint8(side))

faces = sorted(faces,key=lambda b:b[1][1],reverse=False)

face_dict = {}
side = ["top","left","front","back","right","bottom"]
for i in range(6):
    face_dict[side[i]] = faces[i]

cube = CubeClass(face_dict)

finalBottom = [ [[5,2],8], [[5,4],9], [[5,3],10], [[5,1],11] ]


