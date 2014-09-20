from .win import *
from .settings import *
from .colors import *


class CommandWin(Win):
    """
    The command window class
    This class represents the window for a command or other input requests.
    """

    def __init__(self, settings, app, doc, win):
        Win.__init__(self, settings, app, Pos(0, 0))
        self.doc = doc
        self.win = win
        self.disable()

    def draw(self):
        self.clear(self.colors.tabbg)
        w, h = self.settings.userfontsize.t
        textOffset = Pos(10, 12 + h)
        self.drawString(self.doc.mode.promptstring, self.colors.text, Pos(10, 10))
        self.drawString(self.doc.mode.inputstring, self.colors.text, textOffset)
        self.drawCursorLine(textOffset + (w*len(self.doc.mode.inputstring), 0), self.win.flickerCountLeft <= self.settings.flickercount)

    def resize(self, draw=True):
        """Override the resize window"""
        assert draw == False
        s = self.settings
        self.size = s.commandsize
        self.pos = Pos(max(0, (s.size.w - s.commandsize.w) // 2), s.tabsize.h)

    def enable(self):
        Win.enable(self)
        self.win.resetCursor()

    def disable(self):
        Win.disable(self)
        self.win.resetCursor()

