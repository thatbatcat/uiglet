from pyglet.gl import *

#author Ryan Bailey

def clear(color): #color should be an [r,g,b,a] list where every value is 8-bit
    glClearColor(color[0]/255, color[1]/255, color[2]/255, color[3]/255)
    glClear(GL_COLOR_BUFFER_BIT)
