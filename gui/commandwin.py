from .win import *
from .colors import *


class CommandWin(Win):
    """The command window class
    
    This class represents the window for a command.
    """

    def __init__(self, settings, app):
        Win.__init__(self, settings, app, Pos(0, 0), Pos(0, 0))
        self.text = ''
        self.disable()

    def draw(self):
        self.clear(self.colors.tabbg)
        self.drawString(self.text, self.colors.text, 10, 10)

    def onKeyDown(self, c):
        if c == '\n':
            self.disable()
        else:
            self.text += c

    def resize(self, size=None, draw=True):
        """Override the resize window"""
        assert draw == False
        s = self.settings
        self.size = s.commandsize
        self.pos = Pos(max(0, (s.size.w - s.commandsize.w) // 2), s.tabsize.h)
