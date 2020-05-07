import numpy as np
from core.legacy_cube import Cube

faces = []
for i in range(6):
    side = np.loadtxt("temp/side{}.txt".format(i))
    faces.append(np.uint8(side))

face_dict = {}
side = ["top","left","front","back","right","bottom"]
for i in range(6):
    face_dict[side[i]] = faces[i]

cube = Cube(face_dict)

