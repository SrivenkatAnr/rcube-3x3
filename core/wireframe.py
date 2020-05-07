#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun May  3 17:43:20 2020

@author: srivenkat
"""
import pygame as pg
import numpy as np

pg.init()
faces = [np.ones((3,3),np.uint8)for i in range(6)]

class Wireframe:
    def __init__(self):
        self.nodes = np.zeros((0,3))
        self.surfaces = []
        self.nodelist = []
        self.faces = []

    def initNodeList(self,nodeList):
        self.nodelist += nodeList
    
    def initFaces(self,faces):
        self.faces = faces
        top = []
        bottom = []
        front = []
        back = []
        right = []
        left = []
        for i in range(len(self.nodelist)):
            if self.nodelist[i][1] == 3:
                top.append(i) 
            if self.nodelist[i][1] == -3:
                bottom.append(i)
            if self.nodelist[i][2] == -3:
                front.append(i)
            if self.nodelist[i][2] == 3:
                back.append(i)
            if self.nodelist[i][0] == 3:
                right.append(i)                
            if self.nodelist[i][0] == -3:
                left.append(i)
                
        top = np.asarray(self.sortFace(top,0,2,False,True)).reshape(4,4)
        bottom = np.asarray(self.sortFace(bottom,0,2,False,False)).reshape(4,4)
        front = np.asarray(self.sortFace(front,0,1,False,True)).reshape(4,4)
        back = np.asarray(self.sortFace(back,0,1,True,True)).reshape(4,4)
        right = np.asarray(self.sortFace(right,2,1,False,True)).reshape(4,4)
        left = np.asarray(self.sortFace(left,2,1,True,True)).reshape(4,4)
        
        self.com = [top,left,front,right,back,bottom]
        for k in range(len(faces)):
            for i in range(3):
                for j in range(3):            
                    self.addSurfaces([self.nodelist[self.com[k][i][j]],self.nodelist[self.com[k][i][j+1]],self.nodelist[self.com[k][i+1][j]],self.nodelist[self.com[k][i+1][j+1]],faces[k][i][j]])
        self.addNodes(np.asarray(self.nodelist))

    def addNodes(self, node_array):
        if len(self.nodes)==0:
            self.nodes = node_array
        else:
            new = np.zeros((len(self.nodes)+len(node_array),3))
            new[0:len(self.nodes),0:3] = self.nodes
            new[len(self.nodes):,0:3] = node_array
            self.nodes = new
    
    def addSurfaces(self,surface):
        self.surfaces.append(surface)    

    def sortFace(self,face,i,j,h,v):
        face = sorted(face,key=lambda b:self.nodelist[b][i],reverse=h)
        face[0:4] = sorted(face[0:4],key=lambda b:self.nodelist[b][j],reverse=v)
        face[4:8] = sorted(face[4:8],key=lambda b:self.nodelist[b][j],reverse=v)
        face[8:12] = sorted(face[8:12],key=lambda b:self.nodelist[b][j],reverse=v)
        face[12:16] = sorted(face[12:16],key=lambda b:self.nodelist[b][j],reverse=v)
        return face    

    def findCentre(self):
        """ Find the centre of the wireframe. """
        num_nodes = len(self.nodes)
        meanX = sum([node[0] for node in self.nodes]) / num_nodes
        meanY = sum([node[1] for node in self.nodes]) / num_nodes
        meanZ = sum([node[2] for node in self.nodes]) / num_nodes
        return (meanX, meanY, meanZ)  

    def transform(self, matrix):
        """ Apply a transformation defined by a given matrix. """
        centre = self.findCentre()
        self.nodes[:,0] = self.nodes[:,0] - centre[0] 
        self.nodes[:,1] = self.nodes[:,1] - centre[1] 
        self.nodes[:,2] = self.nodes[:,2] - centre[2] 
        self.nodes = np.dot(self.nodes, matrix)    
        self.nodes[:,0] = self.nodes[:,0] + centre[0] 
        self.nodes[:,1] = self.nodes[:,1] + centre[1] 
        self.nodes[:,2] = self.nodes[:,2] + centre[2] 
        self.nodelist = []
        for new_node in self.nodes:
            self.nodelist.append(new_node)
            
    def updateFaces(self,faces):
        self.surfaces = []
        for k in range(len(faces)):
            for i in range(3):
                for j in range(3):            
                    self.addSurfaces([self.nodelist[self.com[k][i][j]],self.nodelist[self.com[k][i][j+1]],self.nodelist[self.com[k][i+1][j+1]],self.nodelist[self.com[k][i+1][j]],faces[k][i][j]])
    
    



    