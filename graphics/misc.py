from pyglet.gl import *

from ...colors import backgroundColor

#author Ryan Bailey

def clear():
    color = backgroundColor()
    glClearColor(color[0]/255, color[1]/255, color[2]/255, color[3]/255)
    glClear(GL_COLOR_BUFFER_BIT)
