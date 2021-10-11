# CENG 487 Assignment2 by
# Erdem Taylan
# StudentId: 240206013
# 12 2020

from OpenGL.raw.GLU import gluLookAt
from vec3d import Vec3d
import math

class Camera:
    def __init__(self,dif):
        """
        cameraPos = Vec3d(0.0, 0.0, 3.0)
        cameraTarget = Vec3d(0.0, 0.0, 0.0)
        cameraDirection = Vec3d.normalize(cameraPos - cameraTarget)
        up = Vec3d(0.0, 1.0, 0.0)
        cameraRight = Vec3d.normalize(Vec3d.cross(up, cameraDirection))
        cameraUp =Vec3d.cross(cameraDirection, cameraRight)"""

        cameraPos = Vec3d(0.0, 0.0, 3.0)
        cameraFront = Vec3d(0.0, 0.0, -1.0)
        cameraUp    = Vec3d(0.0, 1.0, 0.0)
        firstMouse = True

        yaw = -90.0
        pitch =  0.0

        lastX =  800.0 / 2.0
        lastY =  600.0 / 2.0
        fov   =  45.0

        deltaTime = 0.0
        lastFrame = 0.0

        direction=Vec3d(0.0,0.0,0.0)
        direction.x = math.cos(math.radians(yaw)) * math.cos(math.radians(pitch))
        direction.y = math.sin(math.radians(pitch))
        direction.z = math.sin(math.radians(yaw)) * math.cos(math.radians(pitch))

        
        radius = 10.0
        camX = math.sin(dif/20) * radius
        camZ = math.cos(dif/20) * radius
        gluLookAt(camX, 0.0, camZ,0.0, 0.0, 0.0,0.0, 1.0,0.0)