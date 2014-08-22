from .win import *
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
        self.callback = None
        self.disable()

    def draw(self):
        self.clear(self.colors.tabbg)
        self.drawString(self.descr, self.colors.text, Pos(10, 10))
        self.drawString(self.text, self.colors.text, Pos(10, 50))

    def onKeyDown(self, c):
        if c == '\n':
            self.disable()
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

