import math
from pyglet.gl import *

from ..errors import ColorLengthError, ColorRangeError, LackOfVerticesError, ScaleByZeroError

#author Ryan Bailey

class Primitive():
    #color should be an [r,g,b,a] list where every value is 8-bit
    #vertices should be a list of (x,y) tuples
    #rotation should be in degrees
    def __init__(self, color, vertices, screenHeight, rotation=0):
        #some protection is better than no protection, right?
        self.__validateColor(color)
        self.__color = color #note to self: alpha = 0 --> transparent, alpha = 255 --> opaque

        self.__screenHeight = screenHeight

        #remove duplicates of vertices - thanks StackOverflow! beautiful solution!
        used = set()
        self.__vertices = [x for x in vertices if x not in used and (used.add(x) or True)]
        #check there are enough vertices
        if len(vertices) < 3:
            raise LackOfVerticesError("The primitive has too few vertices")
        self.__vertices = vertices

        #convert tuples into lists so that the values can be modified
        self.__color = list(self.__color)
        for i in range(0, len(self.__vertices)):
            self.__vertices[i] = list(self.__vertices[i])

        self.convertVertices()

        if rotation != 0:
            self.rotate(rotation)

    def draw(self):
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        #note to self: (this seems like as good a place as any to put this)

        #when dealing with transparent objects, you need to draw
        #the ones that are furthest away from the camera first
        #and then work your way in to the ones closest to the
        #camera. otherwise the part of a transparent object that
        #is behind another transparent object won't be rendered.

        #that is for 3d space but I'm leaving it here in case
        #it ever becomes relevant.

        #the only thing we need to remember with 2d space is that
        #transparent objects should be drawn after opaque objects.

        glColor4f(self.__color[0]/255,
                  self.__color[1]/255,
                  self.__color[2]/255,
                  self.__color[3]/255)
        glBegin(GL_POLYGON)
        for vertex in self.__vertices:
            glVertex2f(vertex[0], vertex[1])
        glEnd()

    def rotate(self, degrees):
        radians = math.radians(degrees)

        #time for some good old matrix multiplication

        #essentially where T = theta in degrees
        #and x and y are the coordinates of a vertex,
        #I'm doing the following multiplication to all vertices:
        #new vertex = rotation matrix * old vertex, so:

        # (xNew)    =    (cosT  -sinT)    *    (x)
        # (yNew)         (sinT   cosT)         (y)

        #note that the above depiction is of 3 matrices drawn over 2 lines

        #the thing is however, the rotation matrix rotates the object about
        #the origin, so what the above code would do is not rotate the object
        #about its centre, but rather (0, 0), meaning the object is not only
        #rotated, but also translated.

        #to avoid this, before rotating the object, I centre it about the
        #origin. then I rotate it, and then translate it back to it's
        #original position.

        #first figure out where the centre of the object is.
        centreX, centreY = self.getCentre()

        #translate the object so that it is centred about the origin
        for i in range(0, len(self.__vertices)):
            self.__vertices[i][0] -= centreX
            self.__vertices[i][1] -= centreY

        #rotate the object!
        for i in range(0, len(self.__vertices)):
            x, y = self.__vertices[i]
            xNew = math.cos(radians)*x + -math.sin(radians)*y
            yNew = math.sin(radians)*x + math.cos(radians)*y
            self.__vertices[i] = [xNew, yNew]

        #translate the newly rotated object back to its original position
        for i in range(0, len(self.__vertices)):
            self.__vertices[i][0] += centreX
            self.__vertices[i][1] += centreY

    #translate the primitive relative to its current position
    def translateRelative(self, dx, dy):
        for i in range(0, len(self.__vertices)):
            self.__vertices[i][0] += dx
            self.__vertices[i][1] -= dy

    #translate the centre point of the primitive to the specified coordinates
    def translateCenterTo(self, x, y):
        contertedY = self.__screenHeight - y
        centreX, centreY = self.getCentre()
        dx = x - centreX
        dy = contertedY - centreY
        for i in range(0, len(self.__vertices)):
            self.__vertices[i][0] += dx
            self.__vertices[i][1] += dy

    #scales about the centre point
    def scale(self, xScaleFactor, yScaleFactor):
        if xScaleFactor == 0 or yScaleFactor == 0:
            raise ScaleByZeroError("Why would you ever want to scale a primitive by zero?")

        #first figure out where the centre of the object is.
        centreX, centreY = self.getCentre()

        #translate the object so that it is centred about the origin
        for i in range(0, len(self.__vertices)):
            self.__vertices[i][0] -= centreX
            self.__vertices[i][1] -= centreY

        #scale the object!
        for i in range(0, len(self.__vertices)):
            self.__vertices[i][0] *= xScaleFactor
            self.__vertices[i][1] *= yScaleFactor

        #translate the newly scaled object back to its original position
        for i in range(0, len(self.__vertices)):
            self.vertices[i][0] += centreX
            self.vertices[i][1] += centreY

    #color should be an (r,g,b,a) tuple where every value is 8-bit
    def changeColor(self, color):
        self.__validateColor(color)
        self.__color == color

    #figure out where the centre of the object is
    #returns the centre coordinate as an (x, y) tuple
    def getCentre(self):
        minX, minY = self.__vertices[0]
        maxX, maxY = self.__vertices[0]
        for vertex in self.__vertices:
            if vertex[0] < minX:
                minX = vertex[0]
            elif vertex[0] > maxX:
                maxX = vertex[0]
            if vertex[1] < minY:
                minY = vertex[1]
            elif vertex[1] > maxY:
                maxY = vertex[1]
        centreX = (minX + maxX)/2
        centreY = (minY + maxY)/2
        return (centreX, centreY)

    #opengl has the y axis being lowest at the bottom and highest at the top
    #the vertices given presume that the y axis is lowest at the top and highest
    #at the bottom.
    #this function converts these vertices for opengl so they'll display correctly
    def convertVertices(self):
        for i in range(0, len(self.__vertices)):
            y = self.__vertices[i][1]
            self.__vertices[i][1] = self.__screenHeight - y

    def __validateColor(self, color):
        if len(color) != 4:
            raise ColorLengthError("The color supplied to a primitive should have 4 values")
        for dimension in color:
            if dimension < 0 or dimension > 255:
                raise ColorRangeError("The RGB values in the color should be from 0-255")

class Line(Primitive):
    def __init__(self, color, x1, y1, x2, y2, lineWidth, screenHeight):
        dx = x2 - x1
        dy = y2 - y1
        length = math.hypot(dx, dy)
        height = lineWidth
        centreX = (x1 + x2)/2
        centreY = (y1 + y2)/2
        leftX = centreX - length/2
        rightX = centreX + length/2
        topY = centreY - lineWidth/2
        bottomY = centreY + lineWidth/2
        vertices = [(leftX, topY),
                    (leftX, bottomY),
                    (rightX, bottomY),
                    (rightX, topY)]
        rotation = math.atan(dy/dx)#?
        super().__init__(color, vertices, screenHeight, rotation)

class Triangle(Primitive):
    def __init__(self, color, x1, y1, x2, y2, x3, y3, screenHeight):
        vertices = [(x1, y1), (x2, y2), (x3, y3)]
        super().__init__(color, vertices, screenHeight)

class Rectangle(Primitive):
    def __init__(self, color, x, y, width, height, screenHeight, rotation=0):

        vertices = [(x, y),
                    (x + width, y),
                    (x + width, y + height),
                    (x, y + height)]
        super().__init__(color, vertices, screenHeight, rotation)

class Ellipse(Primitive):
    def __init__(self, color, x, y, width, height, screenHeight, rotation=0):
        #(x, y) is the coordinate of the top left corner of the rectangle
        #that fits around the ellipse
        vertexCount = 30
        centreX = x + width/2
        centreY = y + height/2
        vertices = []
        for i in range(0, vertexCount):
            x = centreX + (width/2)*math.cos(i*2*math.pi/vertexCount)
            y = centreY + (height/2)*math.sin(i*2*math.pi/vertexCount)
            vertices += [(x, y)]
        super().__init__(color, vertices, screenHeight, rotation)
