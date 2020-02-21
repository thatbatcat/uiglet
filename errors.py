#author Ryan Bailey

#custom errors

class ScreenAlreadyExistsError(Exception):
    pass

class ScreenDoesntExistError(Exception):
    pass

class NoChangeScreenSpecifiedError(Exception):
    pass

class ColorLengthError(Exception):
    pass

class ColorRangeError(Exception):
    pass

class LackOfVerticesError(Exception):
    pass

class ScaleByZeroError(Exception):
    pass
