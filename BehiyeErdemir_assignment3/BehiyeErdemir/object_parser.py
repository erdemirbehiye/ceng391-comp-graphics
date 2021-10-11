# CENG 487 Assignment3 by
# Behiye Erdemir
# StudentId: 240206013
# 12 2020


from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from mat3d import *
from vec3d import Vec3d
from object import object 
import sys
import numpy as np
from camera import *
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
                    verticeList.append(Vec3d(float(split[1]),float(split[2]),float(split[3]),1))
                elif split[0] == "f":
                    facesList.append((int(split[1]),int(split[2]),int(split[3]),int(split[4])))

        return verticeList, facesList

    @staticmethod
    def draw_obj(theobj,facesList):
        glBegin(GL_QUADS)
        glColor3f(255.0,0.0,0.0)
        for face in facesList:
            for Vertex in face:
                position=theobj.position()+theobj.vertice().__getitem__(Vertex-1)
                glVertex3f(position.x,position.y,position.z)

        glEnd()