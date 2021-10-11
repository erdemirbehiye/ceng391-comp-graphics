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
from mat3d import *
from vec3d import *
from typing import List

def Cube():
    cube=object(pos=Vec3d(0,0,0,0), vertices=[Vec3d(1.0,1.0,1.0,1.0),Vec3d(1.0,1.0,-1.0,1.0),Vec3d(1.0,-1.0,-1.0,1.0),Vec3d(1.0,-1.0,1.0,1.0),Vec3d(-1.0,1.0,1.0,1.0),Vec3d(-1.0,-1.0,-1.0,1.0),Vec3d(-1.0,-1.0,1.0,1.0),Vec3d(-1.0,1.0,-1.0,1.0)])
    cubeEdges = ((0,1),(0,3),(0,4),(1,2),(1,7),(2,5),(2,3),(3,6),(4,6),(4,7),(5,6),(5,7))
    cubeQuads = ((0,3,6,4),(2,5,6,3),(1,2,5,7),(1,0,4,7),(7,4,6,5),(2,3,0,1))
    cube.letsdance([yz_r_Matrix(math.pi/2),t_Matrix(5, 2, 0),s_Matrix(0.2,0.2,0.2)]) #pers(0.1,100,20,0,0,20),
    glBegin(GL_QUADS)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [1,0,0,1])
    glMaterialf(GL_FRONT, GL_SHININESS, 90.0)
    for cubeQuad in cubeQuads:
        for cubeVertex in cubeQuad:
            position=cube.position()+cube.vertice().__getitem__(cubeVertex)
            glVertex3f(position.x,position.y,position.z)

    glEnd()
    glBegin(GL_LINES)
    glColor3f(0.0,0.0,0.0)
    for cubeEdge in cubeEdges:
        for cubeVertex in cubeEdge:
            position=cube.position()+cube.vertice().__getitem__(cubeVertex)
            glVertex3f(position.x,position.y,position.z)
    glEnd()
    #cube.letsdance([t_Matrix(-1, 1, 0), xy_r_Matrix(dif/500), t_Matrix(1, -1, 0)])


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
            sphereNormals.append((Vec3d(x * zr0,y * zr0,z0)))
            sphereNormals.append((Vec3d(x * zr1,y * zr1,z1)))
    
    return sphereVertices, sphereNormals


def sphere(dif,Sphere,atts:List):
    #Sphere.letsdance([t_Matrix(atts[0][1].x, atts[0][1].y,0), yz_r_Matrix(dif/500), t_Matrix(-atts[0][1].x, -atts[0][1].y, 0)])
    glColor3f(1.0,3.0,0.0)
    glBegin(GL_QUAD_STRIP)
    for j in range(len(atts[0])):
        position=Sphere.position()+Sphere.vertice().__getitem__(j)
        glNormal3f(atts[1][j].x,atts[1][j].y,atts[1][j].z)
        glVertex3f(position.x,position.y,position.z)
        
    glEnd()
    return position


def draw_cylinder(radius, height, slice):
    r = radius
    h = height
    n = float(slice)

    circle_pts = []
    for i in range(int(n) + 1):
        angle = 2 * math.pi * (i/n)
        x = r * math.cos(angle)
        y = r * math.sin(angle)
        pt = (x, y)
        circle_pts.append(pt)

    glBegin(GL_TRIANGLE_FAN)#drawing the back circle
    glColor(1, 0, 0)
    glVertex(0, 0, h/2.0)
    for (x, y) in circle_pts:
        z = h/2.0
        glVertex(x, y, z)
    glEnd()

    glBegin(GL_TRIANGLE_FAN)#drawing the front circle
    glColor(0, 0, 1)
    glVertex(0, 0, h/2.0)
    for (x, y) in circle_pts:
        z = -h/2.0
        glVertex(x, y, z)
    glEnd()

    glBegin(GL_TRIANGLE_STRIP)#draw the tube
    glColor(0, 1, 0)
    for (x, y) in circle_pts:
        z = h/2.0
        glVertex(x, y, z)
        glVertex(x, y, -z)
    glEnd()

def initSphere(radius,lat,long):
    atts=calculateSphere(radius,lat,long)
    Sphere=object(pos=Vec3d(0,0,0,0),vertices=atts[0])
    Sphere.letsdance([yz_r_Matrix(math.pi/2),t_Matrix(-5,0,0),s_Matrix(0.2,0.2,0.2)])
    return atts, Sphere
