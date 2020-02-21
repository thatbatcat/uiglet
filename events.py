import pyglet.window.key
import pyglet.window.mouse

#author Ryan Bailey

class Event():
    def __init__(self, type_, modifiers):
        self.__type = type_
        self.__modifers = modifiers

    def type_(self):
        return self.__type

    def controlPressed(self):
        if self.__modifers == None: #MouseScrollEvents and MouseMotionEvents have no modifiers
            return False
        return self.__modifers & pyglet.window.key.MOD_CTRL

    def shiftPressed(self):
        if self.__modifers == None: #MouseScrollEvents and MouseMotionEvents have no modifiers
            return False
        return self.__modifers & pyglet.window.key.MOD_SHIFT

    def altPressed(self):
        if self.__modifers == None: #MouseScrollEvents and MouseMotionEvents have no modifiers
            return False
        return self.__modifers & pyglet.window.key.MOD_ALT

    def capsLockOn(self):
        if self.__modifers == None: #MouseScrollEvents and MouseMotionEvents have no modifiers
            return False
        return self.__modifers & pyglet.window.key.MOD_CAPSLOCK

    def shouldBeProcessed(self):
        return True


class MouseClickEvent(Event):
    def __init__(self, x, y, button, modifiers):
        super().__init__("MOUSE_CLICK", modifiers)
        self.__x = x
        self.__y = y
        self.__button = button

    def leftButtonPressed():
        return self.__button == pyglet.window.mouse.LEFT

    def middleButtonPressed():
        return self.__button == pyglet.window.mouse.MIDDLE

    def rightButtonPressed():
        return self.__button == pyglet.window.mouse.RIGHT

    def location(self):
        return (self.__x, self.__y)

class MouseClickReleaseEvent(Event):
    def __init__(self, x, y, button, modifiers):
        super().__init__("MOUSE_RELEASE", modifiers)
        self.__x = x
        self.__y = y
        #shouldn't need to handle button as you will know which
        #button was pressed from the corresponding MouseClickEvent

    def location(self):
        return (self.__x, self.__y)

class MouseDragEvent(Event):
    def __init__(self, x, y, dx, dy, buttons, modifiers):
        super().__init__("MOUSE_DRAG", modifiers)
        self.__x = x
        self.__y = y
        self.__dx = dx
        self.__dy = dy
        self.__buttons = buttons

    def leftButtonDragged(self):
        return self.__buttons & pyglet.window.mouse.LEFT

    def middleButtonDragged(self):
        return self.__buttons & pyglet.window.mouse.MIDDLE

    def rightButtonDragged(self):
        return self.__buttons & pyglet.window.mouse.RIGHT

    def initialLocation(self):
        return (self.__x, self.__y)

    def finalLocation(self):
        return (self.__x + self.__dx, self.__y + self.__dy)

    def vector(self):
        return (self.__dx, self.__dy)


class KeyEvent(Event):
    def __init__(self, symbol, modifiers):
        super().__init__("KEY_PRESS", modifiers)
        self.__symbol = pyglet.window.key.symbol_string(symbol)
        
    #returns the key pressed
    def key(self):
        if not self.capsLockOn() and self.shiftPressed() and self.isLetter():
            return self.__symbol
        elif self.capsLockOn() and not self.shiftPressed() and self.isLetter():
            return self.__symbol
        elif self.capsLockOn() and self.shiftPressed() and self.isLetter():
            return self.__symbol.lower()
        elif self.isLetter():
            return self.__symbol.lower()
        else:
            return self.__symbol
        #add symbol handling etc?

    def isLetter(self):
        #if the symbol string has a length greater than one, the symbol cannot be a letter
        if len(self.__symbol) > 1:
            return False

        #you only need to check upper case as pyglet always gives the key in upper case
        if int(self.__symbol) >= 65 and int(self.__symbol) <= 90:
            return True
        return False

    #called by app to figure out whether or not the event should be passed to the screen
    def shouldBeProcessed(self):
        alreadyHandled = (pyglet.window.key.LSHIFT,
                          pyglet.window.key.RSHIFT,
                          pyglet.window.key.LCTRL,
                          pyglet.window.key.RCTRL,
                          pyglet.window.key.LALT,
                          pyglet.window.key.RALT,
                          pyglet.window.key.CAPSLOCK)
        if self.__symbol in alreadyHandled:
            return False
        return True

class MouseScrollEvent(Event):
    def __init__(self, x, y, scrollX, scrollY):
        super.__init__("MOUSE_SCROLL", None)
        self.__x = x
        self.__y = y
        #no need to handle scrollX as the app won't be using horizontal scrolling
        self.__scrollY = scrollY

    def mousePosition(self):
        return (self.x, self.y)

    def numberOfScrollClicks(self):
        return scrollY

class MouseMotionEvent(Event):
    def __init__(self, x, y, dx, dy):
        super().__init__("MOUSE_MOTION", None)
        self.__x = x
        self.__y = y
        self.__dx = dx
        self.__dy = dy

    def initialLocation(self):
        return (self.__x, self.__y)

    def finalLocation(self):
        return (self.__x + self.__dx, self.__y + self.__dy)

    def vector(self):
        return (self.__dx, self.__dy)
