# CENG 487 Assignment3 by
# Behiye Erdemir
# StudentId: 240206013

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from mat3d import *
from vec3d import Vec3d
from object import object 
import sys
import numpy as np
from mat3d import *
from typing import List
from vec3d import Vec3d
from os.path import exists, splitext, isfile

class object_parser:
    
    @staticmethod
    def parser(file):
        verticeList=[]
        facesList=[]

        with open(file,"r") as in_file:
            for line in in_file:
                split = line.split()
                if not len(split): #for blank lines
                    continue
                if split[0] == "v":
                    verticeList.append([float(split[1]),float(split[2]),float(split[3]),1])
                elif split[0] == "f":
                    facesList.append([int(split[1])-1,int(split[2])-1,int(split[3])-1,int(split[4])-1])
        return verticeList, facesList

    @staticmethod
    def vextoVec(vertices):
        vec_vertices=[]
        for i in vertices:
            vec_vertices.append(Vec3d(i[0],i[1],i[2],1))
        return vec_vertices

    @staticmethod
    def draw_obj(theobj,facesList):
        colors = (
        (1,0,0),
        (0,1,0),
        (0,0,1),
        (0,1,0),
        (1,1,1),
        (0,1,1),
        (1,0,0),
        (0,1,0),
        (0,0,1),
        (1,0,0),
        (1,1,1),
        (0,1,1),
        )
        glBegin(GL_QUADS)
        for face in facesList:
            x=0
            for Vertex in face:
                x+=1
                glColor3fv(colors[x])
                position=theobj.position()+theobj.vertice().__getitem__(Vertex)
                glVertex3f(position.x,position.y,position.z)

        glEnd()
        
    
        