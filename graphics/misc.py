from pyglet.gl import *

#author Ryan Bailey

def clear(color): #color is an rgba tuple with each value going from 0 --> 255 
    glClearColor(color[0]/255, color[1]/255, color[2]/255, color[3]/255)
    glClear(GL_COLOR_BUFFER_BIT)
