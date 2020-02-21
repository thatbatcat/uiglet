#author Ryan Bailey

class Widget():
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def draw(self):
        raise NotImplementedError("The widget's draw function has not been implemented")

    #should return True if the x, y coordinates provided are inside the widget
    #to be defined for each widget as every widget could be a different shape
    def mousedOver(self, x, y):
        raise NotImplementedError("The widget's mouseOver function has not been implemented")
