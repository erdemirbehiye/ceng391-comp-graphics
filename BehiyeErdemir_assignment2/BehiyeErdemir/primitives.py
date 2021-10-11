# CENG 487 Assignment2 by
# Erdem Taylan
# StudentId: 240206013
# 12 2020

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from vec3d import Vec3d
from object import object 
from mat3d import *
from vec3d import *
import numpy as np
import math

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
    
    
def Cube():
    verticesList=[]
    #define the length of the edge by size/2
    size=2
    """
    Create an array of integers from 0 to 2**N-1.
    e.g. N-1=3
    Convert the integers to binary (becomes [1, 1, 0]).
    Multiply the binary array by 2 and subtract 1 to convert from 0 and 1 to -1 and 1.
    """
    v=size*((np.arange(2**3)[:,None] & (1 << np.arange(3))) > 0) - (size-(size/2))
    for index in v:
        verticesList.append(Vec3d(index[0],index[1],index[2],1))
    cube=object(pos=Vec3d(0,0,0,0), vertices=verticesList)
    cubeQuads = ((0,1,3,2),(2,6,7,3),(0,4,6,2),(4,5,7,6),(4,5,1,0),(5,1,3,7))
    cube.letsdance([yz_r_Matrix(math.pi/2),t_Matrix(5, 2, 0),s_Matrix(0.2,0.2,0.2)]) 
    glBegin(GL_QUADS)
    glColor3f(255.0,0.0,0.0)
    for cubeQuad in cubeQuads:
        x=0
        for cubeVertex in cubeQuad:
            glColor3fv(colors[x])
            position=cube.position()+cube.vertice().__getitem__(cubeVertex)
            glVertex3f(position.x,position.y,position.z)
            x+=1
    glEnd()
     
def calculateSphere( r,  lats,  longs): 
    sphereVertices=[]
    sphereNormals=[]
    for i in range(lats+1):   
        lat0 = math.pi * (-0.5 + (i - 1) / lats)
        z0  = math.sin(lat0)
        zr0 =  math.cos(lat0)

        lat1 = math.pi * (-0.5 + i / lats)
        z1 = math.sin(lat1)
        zr1 = math.cos(lat1)

        for j in range(longs+1):
            lng = 2 * math.pi *(j - 1) / longs
            x = math.cos(lng)
            y = math.sin(lng)
            sphereVertices.append((Vec3d(r * x * zr0,r * y * zr0,r * z0,1)))
            sphereVertices.append((Vec3d(r * x * zr1,r * y * zr1,r * z1,1)))
    
    return sphereVertices

def Sphere(slice):
    radius=2
    lat=slice
    long=slice
    atts=calculateSphere(radius,lat,long)
    Sphere=object(pos=Vec3d(0,0,0,0),vertices=atts)
    Sphere.letsdance([yz_r_Matrix(math.pi/2),t_Matrix(-5,0,0),s_Matrix(0.2,0.2,0.2)])
    #draw the cube
    glBegin(GL_QUAD_STRIP)
    for j in range(len(atts)):
        glColor3fv(colors[j%len(colors)])
        position=Sphere.position()+Sphere.vertice().__getitem__(j)
        glVertex3f(position.x,position.y,position.z)
        
    glEnd()

def Cylinder(slice):
    r = 1
    h = 5
    n = slice #slice number
    points = []
    for i in range(int(n) + 1):
        angle = 2 * math.pi * (i/n)
        x = r * math.cos(angle)
        y = r * math.sin(angle)
        pt = (x, y)
        points.append(pt)
    verticeList=[]
    verticeList.append(Vec3d(0,0,h/2.0,1))
    for (x,y) in points:
        verticeList.append(Vec3d(x,y,h/2.0,1))
    verticeList.append(Vec3d(0,0,h/2.0,1))
    for (x,y) in points:
        verticeList.append(Vec3d(x,y,-h/2.0,1))
    for (x,y) in points:
        verticeList.append(Vec3d(x,y,h/2.0,1))
        verticeList.append(Vec3d(x,y,-h/2.0,1))
    Cylinder=object(pos=Vec3d(0,0,0,0),vertices=verticeList)
    Cylinder.letsdance([t_Matrix(+2,-2,-8)])

    #circles
    glBegin(GL_TRIANGLE_FAN)
    for i in range(2*len(points)+2):
        glColor3fv(colors[0])
        position=Cylinder.position()+Cylinder.vertice().__getitem__(i)
        glVertex3f(position.x,position.y,position.z)
    glEnd()

    #tube
    glBegin(GL_TRIANGLE_STRIP)
    a=0
    for j in range(len(verticeList)-(2*len(points)+2)):
        glColor3fv(colors[a%len(colors)])
        position=Cylinder.position()+Cylinder.vertice().__getitem__(2*len(points)+2+j)
        glVertex3f(position.x,position.y,position.z)
        a+=1
    glEnd()
    return Cylinder

def Torus(slice):
    N=slice*10

    theta=np.linspace(0,2*math.pi,N)
    phi=np.linspace(0,2*math.pi,N)
    o=2
    i=1
    x=[]
    y=[]
    z=[]
    verticeList=[]
    for a in range(N):
        for b in range(N):
            x=(o+i*math.cos(theta[a]))*math.cos(phi[b])
            y=(o+i*math.cos(theta[a]))*math.sin(phi[b])
            z=i*math.sin(theta[a])
            verticeList.append(Vec3d(x,y,z,1))
    
    Torus=object(pos=Vec3d(0,0,0,0),vertices=verticeList)
    Torus.letsdance([t_Matrix(-6,-3,-8)])

    #circles
    
    glBegin(GL_LINES)
    x=0
    for i in range(len(verticeList)):
        glColor3fv(colors[x%len(colors)])
        position=Torus.position()+Torus.vertice().__getitem__(i)
        glVertex3f(position.x,position.y,position.z)
        x+=1
    glEnd()