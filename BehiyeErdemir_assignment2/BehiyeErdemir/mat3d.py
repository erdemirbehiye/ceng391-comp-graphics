# CENG 487 Assignment2 by
# Erdem Taylan
# StudentId: 240206013
# 12 2020

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from vec3d import Vec3d
import math

#Matrix class for initializing matrix and matrix operations
class Mat3d:

    #initialization of a matrix, and its element
    def __init__(self, a: Vec3d, b: Vec3d, c: Vec3d, d: Vec3d):

        self.matrix = [a, b, c, d]
    
    #adding operation for two matrices
    def __add__(self,other: Vec3d):
        return Mat3d(Vec3d(self.matrix[0]+other.matrix[0]),
                     Vec3d(self.matrix[1]+other.matrix[1]),
                     Vec3d(self.matrix[2]+other.matrix[2]),
                     Vec3d(self.matrix[3]+other.matrix[3]))

    #multiplication of a matrix and a scalar
    def __mul__(self, other):
        return Mat3d(self.matrix[0] * other,
                     self.matrix[1] * other,
                     self.matrix[2] * other,
                     self.matrix[3] * other)

    #product of a matrix and vector
    def multiply(self, other: Vec3d):
        return Vec3d(self.matrix[0].dot(other),
                     self.matrix[1].dot(other),
                     self.matrix[2].dot(other),
                     self.matrix[3].dot(other))

    #transpose of a matrix
    def transpose(self):
        return Mat3d(Vec3d(self.matrix[0].x, self.matrix[1].x, self.matrix[2].x, self.matrix[3].x),
                     Vec3d(self.matrix[0].y, self.matrix[1].y, self.matrix[2].y, self.matrix[3].y),
                     Vec3d(self.matrix[0].z, self.matrix[1].z, self.matrix[2].z, self.matrix[3].z),
                     Vec3d(self.matrix[0].w, self.matrix[1].w, self.matrix[2].w, self.matrix[3].w))

    #string representation of a matrix
    def __str__(self):
        return f"{self.matrix[0]}\n{self.matrix[1]}\n{self.matrix[2]}\n{self.matrix[3]}"

#ranslate matrix
class t_Matrix(Mat3d):

    def __init__(self, x, y, z):
        super().__init__(Vec3d(1, 0, 0, x),
                         Vec3d(0, 1, 0, y),
                         Vec3d(0, 0, 1, z),
                         Vec3d(0, 0, 0, 1))

#Scaling Matrix
class s_Matrix(Mat3d):

    def __init__(self, x, y, z):
        super().__init__(Vec3d(x, 0, 0, 0),
                         Vec3d(0, y, 0, 0),
                         Vec3d(0, 0, z, 0),
                         Vec3d(0, 0, 0, 1))

#Rotation Matrix for x axis
class yz_r_Matrix(Mat3d):

    def __init__(self, phi):
        super().__init__(Vec3d(1, 0, 0, 0),
                         Vec3d(0, math.cos(phi), -math.sin(phi), 0),
                         Vec3d(0, math.sin(phi), math.cos(phi), 0),
                         Vec3d(0, 0, 0, 1))

#Rotation Matrix for y axis
class zx_r_Matrix(Mat3d):

    def __init__(self, theta):
        super().__init__(Vec3d(math.cos(theta), 0, math.sin(theta), 0),
                         Vec3d(0, 1, 0, 0),
                         Vec3d(-math.sin(theta), 0, math.cos(theta), 0),
                         Vec3d(0, 0, 0, 1))

#Rotation Matrix for z axis
class xy_r_Matrix(Mat3d):

    def __init__(self, psi):
        super().__init__(Vec3d(math.cos(psi), -math.sin(psi), 0, 0),
                         Vec3d(math.sin(psi), math.cos(psi), 0, 0),
                         Vec3d(0, 0, 1, 0),
                         Vec3d(0, 0, 0, 1))


class pers(Mat3d):
    def __init__(self,n,f,t,b,l,r):
        super().__init__(Vec3d(2*n/r-1,0,(r+1)/(r-1),0),
                        Vec3d(0,2*n/(t-b),(t+b)/(t-b),0),
                        Vec3d(0,0,-((f+n)/(f-n)),-(2*n*f/(f-n))),
                         Vec3d(0,0,-1,0))
