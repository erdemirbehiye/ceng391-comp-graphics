# CENG 487 Assignment3 by
# Behiye Erdemir
# StudentId: 240206013
# 12 2020

#####################TODO####################
from OpenGL.raw.GLU import gluLookAt
from vec3d import Vec3d
class Camera:
    def __init__(self):
        self.eye=Vec3d(0.0,0.0,0.0) #point
        self.center=Vec3d(0.0,0.0,0.0) #point
        self.up=Vec3d(0.0,0.0,0.0)

        self.fov=45
        self.near=0.1
        self.far=10000

        self.cameraX=Vec3d(0.0,0.0,0.0)
        self.cameraY=Vec3d(0.0,0.0,0.0)
        self.cameraZ=Vec3d(0.0,0.0,0.0)

