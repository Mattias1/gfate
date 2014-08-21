from .win import *
from .commandwin import CommandWin
from .colors import *
from time import sleep
import fate.userinterface


class TextWin(Win, fate.userinterface.UserInterface):
    """
    The text window class
    This class represents the window for a single file.
    """

    def __init__(self, settings, app, doc):
        Win.__init__(self, settings, app)
        fate.userinterface.UserInterface.__init__(self, doc)

        self.commandwin = CommandWin(settings, app)
        self.doc = doc
        self.doc.OnQuit.add(self.onQuit)
        self.doc.OnActivate.add(self.onActivate)
        self.flickercountleft = 1
        self.redraw = False
        self.textoffset = Pos(6, 40)

    def loop(self):
        result = self.redraw
        self.redraw = False
        # Draw cursor
        self.flickercountleft -= 1
        if self.flickercountleft in {0, self.settings.flickercount}:
            if self.flickercountleft == 0:
                self.flickercountleft = self.settings.flickercount * 2
            result = True
        # Draw commandwindow
        if self.commandwin.enabled:
            result = result or self.commandwin.loop()
        # Redraw needed
        return result

    def draw(self):
        # Draw selection (and get the selections text already)
        selectionstext = ''
        w, h = self.settings.userfontsize.t
        for i, (b, e) in enumerate(self.doc.selection):
            if b == e:
                bx, by = self.getCharCoord(b).t
                self.drawcursor(bx, by)
                selectionstext += '{}, {}: 0, '.format(by, bx)
            else:
                (bx, by), (ex, ey) = self.getCharCoord(b).t, self.getCharCoord(e).t
                selectionstext += '{}, {}: {}, '.format(by, bx, e - b)
                if by == ey:
                    self.drawRect(self.colors.selectionbg, self.textoffset + (w*bx, by*h), Size(w*(ex - bx), h))
                else:
                    pass
                if str(self.doc.mode) == 'INSERT':
                    self.drawcursor(bx + len(self.doc.mode.insertions[i]), by)
                elif str(self.doc.mode) == 'SURROUND':
                    self.drawcursor(bx, by)
                    self.drawcursor(ex, ey)
                elif str(self.doc.mode) == 'APPEND':
                    self.drawcursor(ex, ey)

        # Draw text
        self.drawString(self.doc.text, self.colors.text, self.textoffset)

        # Draw statuswin
        self.drawStatusWin(selectionstext)

        # Draw commandwin
        if self.commandwin.enabled:
            self.commandwin.draw()

    def drawcursor(self, cx, cy):
        w, h = self.settings.userfontsize.t
        self.drawcursorline(self.textoffset + (w*cx, h*cy), self.flickercountleft <= self.settings.flickercount)

    def drawStatusWin(self, selectionstext):
        h = self.settings.uifontsize.h + 6
        self.drawHorizontalLine(self.colors.hexlerp(self.colors.tabtext, self.colors.bg, 0.75), self.size.h - h - 1)
        self.drawRect(self.colors.tabbg, Pos(0, self.size.h - h), Size(self.size.w, h))
        h = self.size.h - h + 2
        modestr = 'NORMAL' if not self.doc.mode else str(self.doc.mode)
        selpos = Pos(self.size.w - self.textoffset.x - (len(selectionstext) - 2) * self.settings.uifontsize.w, h)
        self.drawString(self.doc.filename + '' if self.doc.saved else '*', self.colors.tabtext, Pos(self.textoffset.x, h))
        self.drawString(modestr, self.colors.tabtext, Pos(self.size.w * 2 // 3, h))
        self.drawString(selectionstext[:-2], self.colors.tabtext, selpos)

    def getTitle(self):
        return self.doc.filename

    def onKeyDown(self, c):
        if self.commandwin.enabled:
            self.commandwin.onKeyDown(c)

    def resize(self, size=None, draw=True):
        assert draw == False
        Win.resize(self, size, draw)
        try:
            self.commandwin.resize(size, False)
        except:
            pass

    def acceptinput(self):
        return not self.commandwin.enabled

    def getCharCoord(self, n):
        """Return (x, y) coordinates of the n-th character. This is a truly terrible method."""
        # Not a very fast method, especially because it's executed often and loops O(n) in the number of characters,
        # but then Chiel's datastructure for text will probably be changed and then this method has to be changed as well.
        x, y = 0, 0
        text = self.doc.text
        for i in range(n):
            c = text[i]
            x += 1
            if c == '\n': # Can't deal with OSX line endings or word wrap (TODO !)
                y += 1
                x = 0
        return Pos(x, y)

    #
    # Implement UserInterface methods
    #
    def touch(self):
        # This method is called from a different thread (the one fate runs in)
        self.redraw = True

    def notify(self, message):
        # This method is called from a different thread (the one fate runs in)
        pass

    def _getuserinput(self):
        # This method is called from a different thread (the one fate runs in)
        # Block untill you have something
        while not self.inputqueue:
            sleep(self.settings.fps_inv)
        return self.inputqueue.popleft()

    def prompt(self, prompt_string='>'):
        # This method is called from a different thread (the one fate runs in)
        pass

    #
    # Some event handlers
    #
    def onQuit(self, doc):
        doc.ui.app.mainWindow.closeTab(fate.document.documentlist.index(doc))

    def onActivate(self, doc):
        doc.ui.app.mainWindow.enableTab(doc.ui)

    #
    # Implement UI commands
    #
    def command_mode(self, command_string=':'):
        # This method is called from a different thread (the one fate runs in)
        self.commandwin.enable()
