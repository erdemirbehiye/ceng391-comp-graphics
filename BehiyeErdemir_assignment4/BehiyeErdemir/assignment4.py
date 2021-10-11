# CENG 487 Assignment3 by
# Behiye Erdemir
# StudentId: 240206013
# 12 2020
"""
I made use of the information on the https://rosettacode.org/wiki/Catmull%E2%80%93Clark_subdivision_surface
while preparing this assignment.
"""
# Note:
# -----
# This Uses PyOpenGL and PyOpenGL_accelerate packages.  It also uses GLUT for UI.
# To get proper GLUT support on linux don't forget to install python-opengl package using apt
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from mat3d import *
from vec3d import Vec3d
from object import object 
import sys
import argparse
from primitives import *
from mat3d import *
from vec3d import *
from typing import List
from object_parser import *
from subdivision import *
from subdivsurf import subdivision_surfaces
import keyboard


# Some api in the chain is translating the keystrokes to this octal string
# so instead of saying: ESCAPE = 27, we use the following.
ESCAPE = '\033'

# Number of the glut window.
window = 0

#initially 0, for time based rotation
oldTime = 0 

if len(sys.argv) != 3:
    print("Please give input in format: 'python <number of level> <object>'")
    sys.exit()

else:
    iterations = int(sys.argv[1]) 
    verticeList,facesList = object_parser.parser(sys.argv[2])
    output_vertices, output_faces = verticeList, facesList
    for i in range(iterations):
        output_vertices, output_faces = subdivision_surfaces.calc_new_obj(output_vertices, output_faces)
output_vertices=object_parser.vextoVec(output_vertices) 
theobj=object(pos=Vec3d(0,0,0,0), vertices=output_vertices)
#theobj.letsdance([t_Matrix(2,2,0),s_Matrix(0.2,0.2,0.2)]) 
# A general OpenGL initialization function.  Sets all of the initial parameters.
def InitGL(Width, Height):  # We call this right after our OpenGL window is created.
    glClearColor(0.0, 0.0, 0.0, 0.0)  # This Will Clear The Background Color To Black
    glClearDepth(1.0)  # Enables Clearing Of The Depth Buffer
    glDepthFunc(GL_LESS)  # The Type Of Depth Test To Do
    glEnable(GL_DEPTH_TEST)  # Enables Depth Testing
    glShadeModel(GL_SMOOTH)  # Enables Smooth Color Shading

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()  # Reset The Projection Matrix
    # Calculate The Aspect Ratio Of The Window
    gluPerspective(45.0, float(Width) / float(Height), 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)


# The function called when our window is resized (which shouldn't happen if you enable fullscreen, below)
def ReSizeGLScene(Width, Height):
    if Height == 0:  # Prevent A Divide By Zero If The Window Is Too Small
        Height = 1

    glViewport(0, 0, Width, Height)  # Reset The Current Viewport And Perspective Transformation
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width) / float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)


# The main drawing function.
def DrawGLScene():
    global rotation
    #for the time based updating
    global oldTime #initially zero
    dif = glutGet(GLUT_ELAPSED_TIME) - oldTime #gives the interval between now and elapsed time
    oldTime = glutGet(GLUT_ELAPSED_TIME) #to provide the same speed, comment for accelerated speed

    # Clear The Screen And The Depth Buffer
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()  # Reset The View


    # Move Left 1.5 units and into the screen 6.0 units.
    glTranslatef(0, 0, -10.0)
    object_parser.draw_obj(theobj,output_faces)
    theobj.letsdance([t_Matrix(-1, 1, 0), zx_r_Matrix(dif/700), t_Matrix(1, -1, 0)])
    #theobj.letsdance([t_Matrix(-1, 1, 0), zx_r_Matrix(dif/500), t_Matrix(1, -1, 0)])

    # since this is double buffered, swap the buffers to display what just got drawn.
    glutSwapBuffers()

# The function called whenever a key is pressed. Note the use of Python tuples to pass in: (key, x, y)
def keyPressed(*args):
	# If escape is pressed, kill everything.
    if args[0] == ESCAPE:
	    sys.exit()

def main():

    global window
    glutInit(sys.argv)
    # Select type of Display mode:
    #  Double buffer
    #  RGBA color
    # Alpha components supported
    # Depth buffer
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)

    # get a 640 x 480 window
    glutInitWindowSize(640, 480)

    # the window starts at the upper left corner of the screen
    glutInitWindowPosition(0, 0)
    window = glutCreateWindow("CENG487 Assigment 1")

    # Display Func
    glutDisplayFunc(DrawGLScene)

    # When we are doing nothing, redraw the scene.
    glutIdleFunc(DrawGLScene)

    # Register the function called when our window is resized.
    glutReshapeFunc(ReSizeGLScene)

    # Register the function called when the keyboard is pressed.
    #glutKeyboardFunc(keyPressed)

    # Initialize our window.
    InitGL(640, 480)

    # Start Event Processing Engine
    glutMainLoop()


# Print message to console, and kick off the main to get it rolling.
main()
