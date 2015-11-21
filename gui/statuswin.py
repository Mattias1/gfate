from .win import *
from .settings import *
from .colors import *


class StatusWin(Win):
    """
    The status window class
    This class is used to draw the status window
    """

    def __init__(self, settings, app, doc, win):
        Win.__init__(self, settings, app, Pos(0, 0))
        self.doc = doc
        self.win = win

    def draw(self, selectionsText):
        """Draw some stats to the bottom of the text win"""
        h = self.settings.statusheight
        self.drawHorizontalLine(self.colors.hexlerp(self.colors.activetab, self.colors.activetabbg, 0.75), 0)
        self.drawRect(self.colors.activetabbg, Pos(0, 1), Size(self.size.w, h - 1))
        h = self.size.h - h + 2
        # modestr = 'Normal' if not self.doc.mode else str(self.doc.mode)
        # selmodestr = '' if not self.doc.selectmode else str(self.doc.selectmode)
        # selpos = Pos(self.size.w - self.textOffset.x - (len(selectionsText) - 2) * self.settings.uifontsize.w, h)
        # self.drawString(self.doc.filename + ('' if self.doc.saved else '*') + ' ' + self.doc.filetype, self.colors.activetab, Pos(self.textOffset.x, h))
        # self.drawString('{} {}'.format(modestr, selmodestr), self.colors.activetab, Pos(self.size.w * 2 // 3, h))
        # self.drawString(selectionsText[:-2], self.colors.activetab, selpos)

        status = '{} | {} | {} | {} | {}'.format(
           self.win.getTitle(),
           self.doc.filetype,
           self.doc.mode,
           self.doc.selectmode,
           selectionsText[:-2])
        self.drawUIString(status, self.colors.activetab, Pos(self.win.textOffset.x, h))

    def resize(self, draw=True):
        """Override the resize window"""
        assert draw == False
        s = self.settings
        self.size = Size(s.size.w, s.statusheight)
        scrollOffset = self.settings.scrollbarwidth if self.settings.scrollbars in {'both', 'horizontal'} else 0
        self.pos = Pos(0, self.win.size.h + self.win.pos.y + scrollOffset)

