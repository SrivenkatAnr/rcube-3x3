#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun May  3 23:55:09 2020

@author: srivenkat
"""
from core.cube_projector import cubeProjection
from core.wireframe import Wireframe
import numpy as np

faces = []
for i in range(6):
	side = np.loadtxt("matrices/test-temp/side{}.txt".format(i))
	faces.append(np.uint8(side))

faces = sorted(faces,key=lambda b:b[1][1],reverse=False)

cube_nodes = [(x,y,z) for x in range(-3,4,2) for z in range(-3,4,2) for y in range(-3,4,2)]

cube_frame = Wireframe()
cube_frame.initNodeList(cube_nodes)
cube_frame.initFaces(faces)

cp = cubeProjection(1000,1000)
cp.addWireframe('cube3D',cube_frame)
cp.run()


sides = cp.cube3D.return2DFaces()
i=0
for side in sides:
	np.savetxt("matrices/test-temp/side{}.txt".format(i),side)
	i+=1