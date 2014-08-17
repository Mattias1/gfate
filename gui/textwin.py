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
        self.cursorvisible = True
        self.textoffset = (6, 40)

    def loop(self):
        self.cursorvisible = not self.cursorvisible
        if self.commandwin.enabled:
            self.commandwin.loop()
        return True

    def draw(self):
        w, h = self.settings.userfontsize
        for b, e in self.doc.selection:
            if b == e:
                x, y = self.getCharCoord(b)
                self.drawcursor(self.textoffset[0] + x, self.textoffset[1] + y, self.cursorvisible)
            else:
                (bx, by), (ex, ey) = self.getCharCoord(b), self.getCharCoord(e)
                if by == ey:
                    self.drawRect(self.colors.selectionbg, self.textoffset[0] + w * bx, self.textoffset[1] + by * h, w * (ex - bx), h)
                else:
                    pass
        self.drawString(self.doc.text, self.colors.text, self.textoffset)
        if self.commandwin.enabled:
            self.commandwin.draw()

    def getTitle(self):
        return self.doc.filename

    def onKeyDown(self, c):
        if self.commandwin.enabled:
            self.commandwin.onKeyDown(c)

    def resize(self, w=None, h=None, draw=True):
        assert draw == False
        Win.resize(self, w, h, draw)
        try:
            self.commandwin.resize(w, h, False)
        except:
            pass

    def acceptinput(self):
        return not self.commandwin.enabled

    def getCharCoord(self, p):
        """Return (x, y) coordinates of the p-th character. This is a truly terrible method."""
        # Not a very fast method, especially because it's executed often and loops O(n) in the number of characters,
        # but then Chiel's datastructure for text will probably be changed and then this method has to be changed as well.
        x, y = 0, 0
        text = self.doc.text
        for i in range(p):
            c = text[i]
            x += 1
            if c == '\n': # Can't deal with OSX line endings... (also: can't deal with word wrap (TODO !))
                y += 1
                x = 0
        return (x, y)

    #
    # Implement UserInterface methods
    #
    def touch(self):
        # This method is called from a different thread (the one fate runs in)
        # TODO: this should be asynchronuous, so don't call draw, but mark it to be drawn later!!!
        self.app.mainWindow.draw()

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
            sleep(1 / self.settings.refresh_rate)
        return self.queue.popleft()

    def peekinput(self):
        # This method is called from a different thread (the one fate runs in)
        # Block untill you have something
        while not self.queue:
            sleep(1 / self.settings.refresh_rate)
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
        pass
