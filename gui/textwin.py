from .win import *
from .commandwin import CommandWin
from .colors import *
from time import sleep
import fate.userinterface


class TextWin(Win, fate.userinterface.UserInterface):
    """The text window class
    
    This class represents the window for a single file.
    """

    def __init__(self, settings, app, document):
        Win.__init__(self, settings, app)

        self.commandwin = CommandWin(settings, app)
        self.doc = document
        self.queue = app.mainWindow.queue
        self.flickercountleft = 1
        self.redraw = False
        self.textoffset = Pos(6, 40)

    def loop(self):
        result = self.redraw
        self.redraw = False
        self.flickercountleft -= 1
        if self.flickercountleft in {0, self.settings.flickercount}:
            if self.flickercountleft == 0:
                self.flickercountleft = self.settings.flickercount * 2
            result = True
        if self.commandwin.enabled:
            result = result or self.commandwin.loop()
        return result

    def draw(self):
        # Draw selection
        w, h = self.settings.userfontsize.t
        for b, e in self.doc.selection:
            if b == e:
                p = self.getCharCoord(b)
                self.drawcursor(self.textoffset + p, self.flickercountleft <= self.settings.flickercount)
            else:
                (bx, by), (ex, ey) = self.getCharCoord(b).t, self.getCharCoord(e).t
                if by == ey:
                    self.drawRect(self.colors.selectionbg, self.textoffset + (w * bx,  + by * h), Size(w * (ex - bx), h))
                else:
                    pass

        # Draw text
        self.drawString(self.doc.text, self.colors.text, self.textoffset)

        # Draw statuswin
        h = self.settings.uifontsize.h + 6
        self.drawHorizontalLine(self.colors.hexlerp(self.colors.tabtext, self.colors.bg, 0.7), self.size.h - h - 1)
        self.drawRect(self.colors.tabbg, Pos(0, self.size.h - h), Size(self.size.w, h))
        selectionstext = ''
        for sel in self.doc.selection:
            selectionstext += str(sel) + ', '
        for i, stat in enumerate(['file: ' + self.doc.filename + '' if self.doc.saved else '*', 'mode: ' + str(self.doc.mode), 'selection: ' + selectionstext[:-2]]):
            self.drawString(stat, self.colors.tabtext, Pos(self.textoffset.x + 300 * i, self.size.h - h + 2))

        # Draw commandwin
        if self.commandwin.enabled:
            self.commandwin.draw()

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

    def activate(self):
        # This method is called from a different thread (the one fate runs in)
        self.app.mainWindow.enableTab(self)

    def getinput(self):
        # This method is called from a different thread (the one fate runs in)
        # Block untill you have something
        while not self.queue:
            sleep(self.settings.fps_inv)
        return self.queue.popleft()

    def peekinput(self):
        # This method is called from a different thread (the one fate runs in)
        # Block untill you have something
        while not self.queue:
            sleep(self.settings.fps_inv)
        return self.queue[0]

    def prompt(self, prompt_string='>'):
        # This method is called from a different thread (the one fate runs in)
        pass

    #
    # Implement UI commands
    #
    def command_mode(self, command_string=':'):
        # This method is called from a different thread (the one fate runs in)
        self.commandwin.enable()
