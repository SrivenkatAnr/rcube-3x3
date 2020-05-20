import pygame
import pygame.locals as pylocals

import threading
import sys
import random
import time

from core.cube_3d import Cube3D
import numpy as np

import OpenGL.GL as gl
import OpenGL.GLU as glu

pygame.init()
window_name = '.'.join(sys.argv[0].split('.')[:-1])
pygame.display.set_caption(window_name if window_name != '' else 'pygame')
pygame.display.gl_set_attribute(pylocals.GL_MULTISAMPLEBUFFERS, 1)
pygame.display.gl_set_attribute(pylocals.GL_MULTISAMPLESAMPLES, 4)
SCREEN = pygame.display.set_mode((800, 600), pylocals.DOUBLEBUF|pylocals.OPENGL)
done = False
clock = pygame.time.Clock()
FRAME_RATE = 120
T_DELAY = 0.5

gl.glEnable(gl.GL_DEPTH_TEST)
gl.glClearColor(54 / 255.0, 54 / 255.0, 54 / 255.0, 0)

glu.gluPerspective(45, 4/3.0, 0.1, 12.0)

gl.glTranslatef(0.0, 0.0, -8.0)

#----------------------------------------------------------------------

<<<<<<< HEAD
faces = {}
side = ["top", "bottom", "left", "right", "front", "back"]
colors = [(1, 1, 1), (1, 1, 0), (0, 1, 0), (0, 0, 1), (1, 0, 0), (1, 0.647, 0)]
for i in range(6):
	faces[side[i]] = np.array([[colors[i] for j in range(3)] for k in range(3)])
cube = Cube3D(faces)
=======
faces = []
for i in range(6):
    side = np.loadtxt("matrices/solved/side{}.txt".format(i))
    faces.append(np.uint8(side))

faces = sorted(faces,key=lambda b:b[1][1],reverse=False)

face_dict = {}
side = ["top","left","front","back","right","bottom"]
for i in range(6):
    face_dict[side[i]] = faces[i]

cube = Cube3D(face_dict)
>>>>>>> cube-solver

def draw():
	cube.render()

<<<<<<< HEAD
movements = {'r':("clockwise","right"),\
			'l':("clockwise","left"),\
			 'u':("clockwise","top"),\
			 'f':("clockwise","front"),\
			 'b':("clockwise","back"),\
			 'd':("clockwise","bottom"),\
			 'ri':("counterClockwise","right"),\
			 'li':("counterClockwise","left"),\
			 'ui':("counterClockwise","top"),\
			 'fi':("counterClockwise","front"),\
			 'bi':("counterClockwise","back"),\
			 'di':("counterClockwise","bottom")}
=======
#----------------------------------------------------------------------

def scrambler():
	keys = list(cube.rotations3D_dict.keys())
	print("scramble = ", end = ' ')
	for i in range(20):
		ind = random.randrange(12)
		rot = keys[ind]
		print(rot, end=' ')
		cube.rotations3D_dict[rot](cube)
		time.sleep(0.2)

def solver():
	algo = cube.solve()
	print(algo)
	for rot in algo:
		cube.rotations3D_dict[rot](cube)
		time.sleep(0.2)

def terminal():
	global done
	buff = ""
	print("Enter the rotation key in lowercase, eg, \"ri\" \nEnter \"scramble\" for scrambling \nEnter \"solve\" for solving \nEnter \"exit\" to exit")
	while not done:
		print(buff)
		command = input("\n>>> ")

		if command == "exit":
			done = True
		elif command == "scramble":
			scrambler()
		elif command in cube.rotations3D_dict.keys():
			cube.rotations3D_dict[command](cube)
		elif command == "solve":
			solver()
		else:
			pass

try:
	thread = threading.Thread(target=terminal)
	thread.start()
except:
	print("Error: unable to start thread")
>>>>>>> cube-solver

while not done:
	gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
	gl.glRotatef(1, 3, 1, 0)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True	
<<<<<<< HEAD
		if event.type == pygame.KEYDOWN:
			cmd = pygame.key.name(event.key)
			t = time.time()
			while (time.time() - t)<T_DELAY:
				for event in pygame.event.get():
					if event.type == pygame.KEYDOWN:
						cmd += pygame.key.name(event.key)
			try:
				args = movements[cmd]
				cube.rotate3D(*args)
				print(cmd)
			except:
				pass

=======
>>>>>>> cube-solver
	draw()
	pygame.display.flip()
	clock.tick(FRAME_RATE)

pygame.quit()