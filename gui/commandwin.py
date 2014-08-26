from .win import *
from .settings import *
from .colors import *


class CommandWin(Win):
    """
    The command window class
    This class represents the window for a command or other input requests.
    """

    def __init__(self, settings, app):
        Win.__init__(self, settings, app, Pos(0, 0), Pos(0, 0))
        self.descr = ''
        self.text = ''
        self.result = ''
        self.callback = None
        self.disable()

    def draw(self):
        self.clear(self.colors.tabbg)
        w, h = self.settings.userfontsize.t
        textOffset = Pos(10, 12 + h)
        self.drawString(self.descr, self.colors.text, Pos(10, 10))
        self.drawString(self.text, self.colors.text, textOffset)
        self.drawCursorLine(textOffset + (w*len(self.text), 0), self.app.mainWindow.activeWin.flickerCountLeft <= self.settings.flickercount)

    def onKeyDown(self, c):
        if c == '\n':
            self.disable()
            self.result = self.text
            if self.callback != None:
                self.callback(self.text)
                self.callback = None
        elif c == 'Esc':
            self.disable()
        elif c=='\b':
            self.text = self.text[:-1]
        else:
            self.text += c
        print(self.text)
        # Maybe force the textwindow to draw again (as in: mark redrawing)?

    def resize(self, size=None, draw=True):
        """Override the resize window"""
        assert draw == False
        s = self.settings
        self.size = s.commandsize
        self.pos = Pos(max(0, (s.size.w - s.commandsize.w) // 2), s.tabsize.h)

