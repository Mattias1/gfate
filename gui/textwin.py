from .win import *
from .colors import *


class TextWin(Win):
    """The text window class
    
    This class represents the window for a single file.
    """

    def __init__(self, settings, app, title):
        Win.__init__(self, settings, app)

        self.title = title
        self.cursorvisible = True

    def loop(self):
        self.cursorvisible = not self.cursorvisible
        return True

    def draw(self):
        self.drawString("The layout of the fate GUI.\nThe title of this textwin is '{}'.".format(self.title), self.colors.text, 6, 40)
        self.drawcursor(195, 40)

    def drawcursor(self, x, y):
        if self.cursorvisible:
            self.drawLine(self.colors.text, x, y, x, y+4+self.settings.userfont[1])
