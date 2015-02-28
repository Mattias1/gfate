from .win import *
from .settings import *
from .colors import *
from fate.errorchecking import ErrorMode


class ErrorWin(Win):
    """
    The error window class
    This class represents the window for an error message (compile errors, linter messages, etc).
    """

    def __init__(self, settings, app, doc, win):
        Win.__init__(self, settings, app, Pos(0, 0))
        self.doc = doc
        self.win = win
        # self.disable()

    def draw(self):
        self.clear(self.colors.tabbg)
        w, h = self.settings.userfontsize.t
        textOffset = Pos(10, 12 + h)

        # Draw title
        self.drawHorizontalLine(self.colors.hexlerp(self.colors.tabtext, self.colors.bg, 0.75), 0)
        self.drawUIString("Error list", self.colors.text, Pos(0, 2))
        self.drawHorizontalLine(self.colors.hexlerp(self.colors.tabtext, self.colors.bg, 0.75), h + 4)

        # Draw errors
        for i, (errortype, interval, message) in enumerate(self.doc.errorlist):
            bgColor = self.colors.selectionbg if self.doc.errorlist.current == i else self.colors.bg
            column, line = self.win.getCoordFromChar(interval[0]).t
            self.drawString('{} at {},{}: {}'.format(errortype, line, column, message), self.colors.text, Pos(0, i*h + h + 6))

    def loop(self):
        # We only want to be enabled if errormode is active.
        if isinstance(self.doc.mode, ErrorMode) and not self.enabled:
            self.enable()
        if not isinstance(self.doc.mode, ErrorMode) and self.enabled:
            # self.disable()
            pass

    def resize(self, draw=True):
        """Override the resize window"""
        assert draw == False
        s = self.settings
        self.size = s.commandsize
        self.pos = Pos(max(0, (s.size.w - s.commandsize.w) // 2), s.tabsize.h)

