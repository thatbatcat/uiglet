import pyglet
import os.path

#author Ryan Bailey

class Label(pyglet.text.Label):
    def __init__(self, text, color, size, x, y, width, height, screenHeight, anchor_x="left", anchor_y="top"):
        #opengl has the y axis being lowest at the bottom and highest at the top
        #the y value given presumes that the y axis is lowest at the top and highest
        #at the bottom.
        #the following line converts the y value for opengl
        #so the label will display correctly
        cY = screenHeight - y

        super().__init__(text=text,
                         color=color,
                         font_size=size,
                         x=x,
                         y=cY,
                         width=width,
                         height=height,
                         font_name="Courier",
                         anchor_x=anchor_x,
                         anchor_y=anchor_y)


#dpi is dots per inch or pixels per inch
#font size is in points
#a point is 1/72 of an inch
#therefore pixels per point = dpi/72
#total pixels = points*dpi/72
#font size = pixels*72/dpi

#converts pixels to points
def pixelsToPoints(self, heightInPixels):
        self.font_size = math.floor(heightInPixels*72/self.dpi)
