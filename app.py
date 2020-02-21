import pyglet

from .events import *
from .errors import ScreenAlreadyExistsError, ScreenDoesntExistError
from .graphics.misc import clear

#author Ryan Bailey

#on_draw, on_mouse_press, on_mouse_release, on_key_press,
#on_mouse_drag, on_mouse_motion and on_mouse_scroll
#are overridden functions that are called by pyglet

class App(pyglet.window.Window):
    def __init__(self, title="Window!"):
        super().__init__(caption=title, fullscreen=True)

        self.__screens = []
        self.__screen = None

    def addScreen(self, name, screen):
        for screen in self.__screens:
            if screen[0] == name:
                raise ScreenAlreadyExistsError("(App.addScreen) A Screen with the name " + name + " already exists")

        self.__screens += [(name, screen)]

    def setScreen(self, name):
        for screen in self.__screens:
            if screen[0] == name:
                self.__screen = screen[1]
                return

        raise ScreenDoesntExistError("(App.setScreen) The Screen " + name + "does not exist")

    def on_draw(self):
        if self.__screen == None:
            return

        clear()
        self.__screen.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        mouseClickEvent = MouseClickEvent(x, y, button, modifiers)
        if mouseClickEvent.shouldBeProcessed():
            self.__screen.processInput(mouseClickEvent)
        self.handleScreenRequests()

    def on_mouse_release(self, x, y, button, modifiers):
        mouseClickReleaseEvent = MouseClickReleaseEvent(x, y, button, modifiers)
        if mouseClickReleaseEvent.shouldBeProcessed():
            self.__screen.processInput(mouseClickReleaseEvent)
        self.handleScreenRequests()

    def on_key_press(self, symbol, modifiers):
        keyEvent = KeyEvent(symbol, modifiers)
        if keyEvent.shouldBeProcessed():
            self.__screen.processInput(keyEvent)
        self.handleScreenRequests()

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        mouseDragEvent = MouseDragEvent(x, y, dx, dy, buttons, modifiers)
        if mouseDragEvent.shouldBeProcessed():
            self.__screen.processInput(mouseDragEvent)
        self.handleScreenRequests()

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        mouseScrollEvent = MouseScrollEvent(x, y, scroll_x, scroll_y)
        if mouseScrollEvent.shouldBeProcessed():
            self.__screen.processInput(mouseScrollEvent)
        self.handleScreenRequests()

    def on_mouse_motion(self, x, y, dx, dy):
        mouseMotionEvent = MouseMotionEvent(x, y, dx, dy)
        if mouseMotionEvent.shouldBeProcessed():
            self.__screen.processInput(mouseMotionEvent)
        self.handleScreenRequests()

    #handle requests made by the current screen
    #should be called by App's input handling functions
    def handleScreenRequests(self):
        if self.__screen.screenChangeRequested():
            self.setScreen(self.__screen.changeScreen())
        if self.__screen.closeRequested():
            self.close()

    #to be called after a screen has been added and set
    def run(self):
        pyglet.app.run()

    #for debug
    def availableScreens(self):
        print("AVAILABLE SCREENS")
        for screen in self.__screens:
            print("\t" + screen[0])
