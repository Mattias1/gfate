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

    def loop(self):
        self.cursorvisible = not self.cursorvisible
        if self.commandwin.enabled:
            self.commandwin.loop()
        return True

    def draw(self):
        self.drawString(self.doc.text, self.colors.text, 6, 40)
        self.drawcursor(195, 40)
        if self.commandwin.enabled:
            self.commandwin.draw()

    def drawcursor(self, x, y):
        if self.cursorvisible:
            self.drawLine(self.colors.text, x, y, x, y+4+self.settings.userfont[1])

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

    #
    # Implement UserInterface methods
    #
    def touch(self):
        # This method is called from a different thread (the one fate runs in)
        # TODO: this should be asynchronuous, so don't call draw, but mark it to be drawn later!!!
        self.draw()

    def notify(self, message):
        # This method is called from a different thread (the one fate runs in)
        pass

    def activate(self):
        # This method is called from a different thread (the one fate runs in)
        pass

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

    def activate(self):
        # This method is called from a different thread (the one fate runs in)
        self.app.mainWindow.enableTab(self)
