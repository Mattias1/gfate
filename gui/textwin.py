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
        Win.__init__(self, settings, app, Pos(0, settings.tabsize.h))
        fate.userinterface.UserInterface.__init__(self, doc)

        self.commandWin = CommandWin(settings, app)
        self.doc = doc
        self.doc.OnQuit.add(self.onQuit)
        self.doc.OnActivate.add(self.onActivate)
        self.flickerCountLeft = 1
        self.redraw = False
        self.textOffset = Pos(6, 4)

    def loop(self):
        result = self.redraw
        self.redraw = False
        # Draw cursor
        self.flickerCountLeft -= 1
        if self.flickerCountLeft in {0, self.settings.flickercount}:
            if self.flickerCountLeft == 0:
                self.flickerCountLeft = self.settings.flickercount * 2
            result = True
        # Draw commandWindow
        if self.commandWin.enabled:
            result = result or self.commandWin.loop()
        # Redraw needed
        return result

    def draw(self):
        # Draw selection (and get the selections text already)
        selectionstext = ''
        w, h = self.settings.userfontsize.t
        for i, (b, e) in enumerate(self.doc.selection):
            if b >= e:
                bx, by = self.getCoordFromChar(b).t
                self.drawCursor(bx, by)
                selectionstext += '({}, {}: 0), '.format(by, bx)
            else:
                bx, by = self.getCoordFromChar(b).t
                ex, ey = self.drawSelection(w, h, b, e, bx, by)
                selectionstext += '({}, {}: {}), '.format(by, bx, e - b)
                if 'ChangeBefore' in str(self.doc.mode):
                    self.drawCursor(bx + len(self.doc.mode.peek().insertions[i]), by)
                elif 'ChangeAround' in str(self.doc.mode):
                    self.drawCursor(bx, by)
                    self.drawCursor(ex, ey)
                elif 'ChangeAfter' in str(self.doc.mode):
                    self.drawCursor(ex, ey)

        # Draw text
        self.drawText(self.doc.text, self.doc.labeling)

        # Draw statuswin
        self.drawStatusWin(selectionstext)

        # Draw commandWin
        if self.commandWin.enabled:
            self.commandWin.draw()

    def drawCursor(self, cx, cy):
        w, h = self.settings.userfontsize.t
        self.drawCursorLine(self.textOffset + (w*cx, h*cy), self.flickerCountLeft <= self.settings.flickercount)

    def drawSelection(self, w, h, b, e, bx, by):
        i = b
        while i < e:
            c = self.doc.text[i]
            if i == e - 1 or c == '\n': # TODO: manage different newline options
                self.drawRect(self.colors.selectionbg, self.textOffset + (w*bx, by*h), Size(w*(i + 1 - b), h))
                if i == e - 1:
                    return (bx + i + 1 - b, by)
                bx, by = 0, by + 1
                b = i # Mark the character no. of the selection beginning
            i += 1
        raise Exception('Character at end of selection not found')

    def drawText(self, text, labeling):
        self.drawString(self.doc.text, self.colors.text, self.textOffset)

    def drawStatusWin(self, selectionstext):
        h = self.settings.uifontsize.h + 6
        self.drawHorizontalLine(self.colors.hexlerp(self.colors.tabtext, self.colors.bg, 0.75), self.size.h - h - 1)
        self.drawRect(self.colors.tabbg, Pos(0, self.size.h - h), Size(self.size.w, h))
        h = self.size.h - h + 2
        # modestr = 'Normal' if not self.doc.mode else str(self.doc.mode)
        # selmodestr = '' if not self.doc.selectmode else str(self.doc.selectmode)
        # selpos = Pos(self.size.w - self.textOffset.x - (len(selectionstext) - 2) * self.settings.uifontsize.w, h)
        # self.drawString(self.doc.filename + ('' if self.doc.saved else '*') + ' ' + self.doc.filetype, self.colors.tabtext, Pos(self.textOffset.x, h))
        # self.drawString('{} {}'.format(modestr, selmodestr), self.colors.tabtext, Pos(self.size.w * 2 // 3, h))
        # self.drawString(selectionstext[:-2], self.colors.tabtext, selpos)

        status = '{} | {} | {} | {} | {}'.format(
           self.getTitle(),
           self.doc.filetype,
           self.doc.mode,
           self.doc.selectmode,
           selectionstext[:-2])
        self.drawUIString(status, self.colors.tabtext, Pos(self.textOffset.x, h))

    def getTitle(self):
        return self.doc.filename + ('' if self.doc.saved else '*')

    def onKeyDown(self, c):
        if self.commandWin.enabled:
            self.commandWin.onKeyDown(c)

    def resize(self, draw=True):
        assert draw == False
        self.size = self.settings.size - (0, self.settings.tabsize.h)
        self.commandWin.resize(False)

    def acceptinput(self):
        return not self.commandWin.enabled

    def showCmdWin(self, descr='Command', inpt='', callback=None):
        self.commandWin.descr = descr
        self.commandWin.text = inpt
        self.commandWin.result = ''
        self.commandWin.callback = callback
        self.commandWin.enable()

    def getCoordFromChar(self, n):
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
        self.showCmdWin('Notification: ' + message)

    def _getuserinput(self):
        # This method is called from a different thread (the one fate runs in)
        # Block untill you have something
        while not self.inputqueue:
            sleep(self.settings.fps_inv)
        return self.inputqueue.popleft()

    def prompt(self, prompt_string='>'):
        # This method is called from a different thread (the one fate runs in)
        self.showCmdWin(prompt_string, '', lambda result: print('Prompt result: ' + result))
        while not self.commandWin.result:
            sleep(self.settings.fps_inv)
        return self.commandWin.result

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
        print('THIS METHOD IS ACTUALLY BEING CALLED!!! - def command_mode(...) in textwin.py (bottom of the file)')
        self.showCmdWin('', command_string, lambda result: print(result))

