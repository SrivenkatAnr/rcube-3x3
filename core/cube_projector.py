import pygame
import numpy as np
from .layer3_solver import layer3Solver
from .cube_sim import Cube
import collections
import time
import threading
import random

pygame.init()

colors = [(255, 255, 255), (255,128,0), (0,255,0), (0,0,255), (255,0,0), (255,255,0), (0, 0, 0)]
T_DELAY = 0.3


key_to_function = { pygame.K_LEFT:   (lambda x: x.transformall(x.rotateYMatrix(-15))),
                    pygame.K_RIGHT:  (lambda x: x.transformall(x.rotateYMatrix(15))),
                    pygame.K_DOWN:   (lambda x: x.transformall(x.rotateXMatrix(+15))),
                    pygame.K_UP:     (lambda x: x.transformall(x.rotateXMatrix(-15))),
                    pygame.K_EQUALS: (lambda x: x.transformall(x.rotateZMatrix(+15))),
                    pygame.K_MINUS:  (lambda x: x.transformall(x.rotateZMatrix(-15)))}

class cubeProjection:
#Displays 3D objects on a Pygame screen
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Wireframe Display')
        self.background = (10,10,50)
        self.wireframes = {}
        self.displayNodes = True
        self.displayColors = True
        self.nodeColour = (255,255,255)
        self.edgeColour = (200,200,200)
        self.nodeRadius = 4
        self.cube3D = None
        
    def addWireframe(self,name,frame):
        self.wireframes[name] = frame
        self.define3Dcube()
    
    def define3Dcube(self):
        for wf in self.wireframes.values():
            faces = wf.faces
            face_dict = collections.OrderedDict([("top",None), ("left",None), ("front",None), ("back",None), ("right",None), ("bottom",None)])
            for i in range(6):
                face_dict[list(face_dict.keys())[i]] = faces[i]
            self.cube3D = Cube(face_dict)

    def rotateXMatrix(self,deg):
    # Return matrix for rotating about the x-axis by 'radians' radians
        radians = deg*3.14/180
        c = np.cos(radians)
        s = np.sin(radians)
        return np.array([[1, 0, 0],
                         [0, c,-s],
                         [0, s, c]])
                         
    def rotateYMatrix(self,deg):
    # Return matrix for rotating about the y-axis by 'radians' radians """        
        radians = deg*3.14/180       
        c = np.cos(radians)
        s = np.sin(radians)
        return np.array([[ c, 0, s],
                         [ 0, 1, 0],
                         [-s, 0, c]])

    def rotateZMatrix(self,deg):
    # Return matrix for rotating about the z-axis by 'radians' radians """        
        radians = deg*3.14/180      
        c = np.cos(radians)
        s = np.sin(radians)
        return np.array([[c,-s, 0],
                         [s, c, 0],
                         [0, 0, 1]])
                                  
    def project(self,points):
        new = []
        for pt in points:
            factor = 1000 / (20 + pt[2])
            x = (pt[0])*factor + self.width/2
            y = -(pt[1])*factor + self.height/2
            new.append([x,y,pt[2]])
        return new

    def display(self):
        """ Draw the wireframes on the screen. """
        self.screen.fill(self.background)
        for wireframe in self.wireframes.values():
            if self.displayNodes:
                for node in wireframe.nodes:
                    pygame.draw.circle(self.screen, self.nodeColour, (int(node[0]), int(node[1])), self.nodeRadius, 0)
            if self.displayColors:
                avg_z = []
                for i in range(len(wireframe.surfaces)):
                    item = wireframe.surfaces[i]
                    mean = (item[0][2] +item[1][2] +item[2][2] +item[3][2])/4.0
                    avg_z.append((mean,i))
                for temp in sorted(avg_z,key=lambda b:b[0],reverse=True):
                    surf = wireframe.surfaces[int(temp[1])]
                    surf[:4] = self.project(surf[:4])
                    bound = [tuple(surf[0])[:2],tuple(surf[1])[:2],tuple(surf[2])[:2],tuple(surf[3])[:2]]
                    pygame.draw.polygon(self.screen,colors[int(surf[4])],bound)                
                    pygame.draw.polygon(self.screen,(0,0,0),bound,3) 

    def transformall(self,matrix):
        """ Rotate all wireframe about their centre, along a given axis by a given angle. """
        for wireframe in self.wireframes.values():
            wireframe.transform(matrix)
            
    def updateall(self):
        facelist = self.cube3D.return3DFaces()
        for wireframe in self.wireframes.values():
            wireframe.updateFaces(facelist)
    
    def scrambler(self):
        keys = list(self.cube3D.rotation_dict.keys())
        print("scramble = ", end = ' ')
        for i in range(20):
            ind = random.randrange(12)
            rot = keys[ind]
            print(rot, end=' ')
            self.cube3D.rotation_dict[rot](self.cube3D)
            self.updateall()
            time.sleep(0.2)

    def solver(self):
        faces = self.cube3D.return2DFaces()
        faces = sorted(faces,key=lambda b:b[1][1],reverse=False)
        face_dict = {}
        side = ["top","left","front","back","right","bottom"]
        for i in range(6):
            face_dict[side[i]] = faces[i]

        solver = layer3Solver(face_dict)
        solver.runCubeSolver()
        solver.compressAlgo()
        for rot in solver.algo:
            self.cube3D.rotation_dict[rot](self.cube3D)
            self.updateall()
            time.sleep(0.15)
        print("Solved!!!")
        print(solver.algo)

    def terminal(self):
        buff = ""
        print("Enter the rotation key in lowercase, eg, \"ri\" \nEnter \"scramble\" for scrambling \nEnter \"solve\" for solving \nEnter \"exit\" to exit")
        while self.running:
            print(buff)
            command = input("\n>>> ")

            if command == "exit":
                self.running = False
            elif command == "scramble":
                self.scrambler()
            elif command in self.cube3D.rotation_dict.keys():
                self.cube3D.rotation_dict[command](self.cube3D)
                self.updateall()
            elif command == "solve":
                self.solver()
            else:
                pass

    def run(self):        
        self.running = True
        try:
            thread = threading.Thread(target=self.terminal)
            thread.start()
        except:
            print("Error: unable to start thread")

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False    
                elif event.type == pygame.KEYDOWN:
                    if event.key in key_to_function:
                        key_to_function[event.key](self)                               
            self.screen.fill(self.background)
            self.updateall()
            self.display()
            pygame.display.flip()
            
        pygame.quit()

