from .errors import NoChangeScreenSpecifiedError

#author Ryan Bailey

class Screen():
    def __init__(self):
        self.__state = None
        self.__nextScreen = None
        self.__screenChangeRequested = False
        self.__closeRequested = False

    def draw(self):
        raise NotImplementedError("The current screen's draw function is not implemented")

    def processInput(self, event):
        raise NotImplementedError("The current screen's processInput function is not implemented")

    #use this function to request that the app switch from this screen to another
    def requestScreenChange(self, screenName):
        self.__screenChangeRequested = True
        self.__nextScreen = screenName

    #this is the function that the app uses to test if a screen change has been requested
    def screenChangeRequested(self):
        return self.__screenChangeRequested

    #return the name of the screen to be switched to, and prepare this screen for when it is next switched to.
    #this method should only be called in an App.setScreen function call
    def changeScreen(self):
        if self.__nextScreen == None:
            raise NoChangeScreenSpecifiedError("Cannot change screen as no screen has been specified")
        self.screenChangeRequested = False
        return self.__nextScreen

    #use this function to request that the app close
    def requestClose(self):
        self.__closeRequested = True

    #this is the function that the app uses to test if close has been requested
    def closeRequested(self):
        return self.__closeRequested
