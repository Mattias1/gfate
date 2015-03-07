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
        self.disable()

    def draw(self):
        self.clear(self.colors.tabbg)
        w, h = self.settings.userfontsize.t

        # Draw title
        self.drawHorizontalLine(self.colors.hexlerp(self.colors.tabtext, self.colors.bg, 0.75), 0)
        self.drawUIString("Error list", self.colors.text, Pos(self.win.textOffset.x, 2))
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
            self.resize(False)
        if not isinstance(self.doc.mode, ErrorMode) and self.enabled:
            self.disable()

    def resize(self, draw=True):
        """Override the resize window"""
        assert draw == False
        s = self.settings
        try:
            height = min(1, min(s.maxerrorlines, len(self.doc.errorlist)))
        except:
            height = 1
        height = (height + 1) * s.uifontsize.h + 5
        self.size = Size(self.win.size.w, height)
        scrollOffset = self.settings.scrollbarwidth if self.settings.scrollbars in {'both', 'horizontal'} else 0
        self.pos = Pos(0, self.win.size.h + self.win.pos.y - scrollOffset - height)

