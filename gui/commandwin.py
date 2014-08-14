from .win import *
from .colors import *


class CommandWin(Win):
    """The command window class
    
    This class represents the window for a command.
    """

    def __init__(self, settings, app):
        Win.__init__(self, settings, app, 0, 0, 0, 0)
        self.disable()

    def draw(self):
        self.clear(self.colors.tabbg)
        self.drawString(":quit", self.colors.text, 10, 10)

    def resize(self, w=None, h=None, draw=True):
        """Override the resize window"""
        s = self.settings
        self.width, self.height = s.commandwidth, s.commandheight
        self.x, self.y = max(0, (s.width - s.commandwidth) // 2), s.tabheight
