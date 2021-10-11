# CENG 487 Assignment5 by
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
        normalList=[]
        somelistv=[]
        somelistvn=[]

        with open(file,"r") as in_file:
            for i,line in enumerate(in_file):
                line=line.replace("//"," ")
                split = line.split()
                if not len(split): #for blank lines
                    continue
                if split[0] == "v":
                    verticeList.append([float(split[1]),float(split[2]),float(split[3]),1])
                elif split[0] == "vn":
                    normalList.append([float(split[1]),float(split[2]),float(split[3])])
                elif split[0]=="s":
                    somelistv.append([])
                    somelistvn.append([])
                    continue
                elif split[0] =="f":
                    somelistv[-1].append([int(split[1])-1,int(split[3])-1,int(split[5])-1,int(split[7])-1])
                    somelistvn[-1].append([int(split[2])-1,int(split[4])-1,int(split[6])-1,int(split[8])-1])
            
                    
        return verticeList, normalList, somelistv ,somelistvn

    @staticmethod
    def vextoVec(vertices):
        vec_vertices=[]
        for i in vertices:
            vec_vertices.append(Vec3d(i[0],i[1],i[2],1))
        return vec_vertices

    @staticmethod
    def draw_obj(theobj,normalList,facesList,NormalList):
        glClear(GL_COLOR_BUFFER_BIT)
        colors=[[1,0,0,1],[1,1,1,1],[1,1,1,1],[0,1,0,1],[1,1,1,1],[1,0.5,0.5,1],[1,0.5,0.5,1]]
        x=0
        glBegin(GL_QUADS)
        for i in range(len(facesList)):
            glMaterialfv(GL_FRONT, GL_DIFFUSE, colors[i])
            glMaterialf(GL_FRONT, GL_SHININESS, 90.0)
            facegrup=facesList[i]
            normalgrup=NormalList[i]
            
            x+=1
            for face in facegrup:
                for i,Vertex in enumerate(face):
                    
                    
                    position=theobj.position()+theobj.vertice().__getitem__(Vertex)
                    glNormal3fv(normalList[normalgrup[0][i]])
                    glVertex3f(position.x,position.y,position.z)
                    

        glEnd()
        
    
        