# CENG 487 Assignment3 by
# Behiye Erdemir
# StudentId: 240206013
# 12 2020

from typing import List
from vec3d import Vec3d
from mat3d import *

#object class is for holding the information of position and vertices 
class object:
    #initializes the position and vertice vetors of an object
    def __init__(self, pos: Vec3d, vertices: List[Vec3d]):
        self.pos = pos
        self.x=pos.x
        self.y=pos.y
        self.z=pos.z
        self.vertices = vertices

    #returns the vertices of an abject
    def vertice(self):
        return self.vertices

    #creates the position vector of an object
    def position(self):
        return Vec3d(self.x,self.y,self.z)
    
    def letsdance(self, transforms: List[Mat3d]):  #list for tracking the order of transformations
        for t in transforms: #for each transform matrix
            for i, vertex in enumerate(self.vertices): 
                self.vertices[i] = t.multiply(vertex) #multiply vertices by the transform matrix