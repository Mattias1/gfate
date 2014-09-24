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

        self.commandWin = CommandWin(settings, app, doc, self)
        self.doc = doc
        self.doc.OnQuit.add(self.onQuit)
        self.doc.OnActivate.add(self.onActivate)
        self.flickerCountLeft = 0
        self.redraw = False
        self.oldSelection = self.doc.selection[-1]
        self.textOffset = Pos(6, 4)
        self.displayOffset = Pos(0, 0)
        self.displayIndex = 0
        self.textRange = Size(0, 0)
        self.nrOfLines = 0

    @property
    def displayOffset(self):
        return self._displayOffset
    @displayOffset.setter
    def displayOffset(self, value):
        self._displayOffset = Pos(value)
        self._displayIndex = self.getCharFromCoord(self._displayOffset)

    @property
    def displayIndex(self):
        return self._displayIndex
    @displayIndex.setter
    def displayIndex(self, value):
        self._displayIndex = value
        self._displayOffset = self.getCoordFromChar(value)

    @property
    def cursorRange(self):
        return self.textRange - 2 * self.settings.cursormargin - (0, 1)

    def loop(self):
        result = self.redraw
        # Update some stats for fast access
        if self.redraw:
            self.nrOfLines = len(str(self.doc.text.count('\n')))
        self.redraw = False
        # Show/hide the commandwindow
        if 'Prompt' in str(self.doc.mode) and not self.commandWin.enabled:
            self.commandWin.enable()
        if 'Prompt' not in str(self.doc.mode) and self.commandWin.enabled:
            self.commandWin.disable()
        # Adjust display offset on cursor movement
        if self.oldSelection != self.doc.selection[-1]:
            self.oldSelection = self.doc.selection[-1]
            self.adjustWindow()
            self.resetCursor()
        # Draw commandWindow
        if self.commandWin.enabled:
            result = result or self.commandWin.loop()
        # Draw cursor
        self.flickerCountLeft -= 1
        if self.flickerCountLeft in {0, self.settings.flickercount}:
            if self.flickerCountLeft == 0:
                self.flickerCountLeft = self.settings.flickercount * 2
            result = True
        # Redraw needed
        return result

    def draw(self):
        """Draw the text win"""
        # Draw selection (and get the selections text already)
        selectionstext = ''
        w, h = self.settings.userfontsize.t
        lineNrW = self.calcLineNumberWidth(w)
        for i, (b, e) in enumerate(self.doc.selection):
            if b >= e:
                bx, by = self.getCoordFromChar(b).t
                self.drawCursor(bx, by, lineNrW)
                selectionstext += '({}, {}: 0), '.format(by + 1, bx)
            else:
                bx, by = self.getCoordFromChar(b).t
                ex, ey = self.drawSelection(w, h, b, e, bx, by, lineNrW)
                selectionstext += '({}, {}: {}), '.format(by + 1, bx, e - b)
                if 'ChangeBefore' in str(self.doc.mode):
                    self.drawCursor(bx + len(self.doc.mode.insertions[i]), by, lineNrW)
                elif 'ChangeAround' in str(self.doc.mode):
                    self.drawCursor(bx, by, lineNrW)
                    self.drawCursor(ex, ey, lineNrW)
                elif 'ChangeAfter' in str(self.doc.mode):
                    self.drawCursor(ex, ey, lineNrW)

        # Draw text
        self.drawText(self.doc.text, self.doc.labeling, lineNrW)

        # Draw statuswin
        if self.settings.statuswinenabled:
            self.drawStatusWin(selectionstext)

        # Draw commandWin
        if self.commandWin.enabled:
            self.commandWin.draw()

    def drawCursor(self, cx, cy, lineNrW):
        """Draw a single cursor (that is, an empty selection)"""
        ox, oy = self.displayOffset.t
        if not oy <= cy <= oy + self.textRange.h:
            return
        w, h = self.settings.userfontsize.t
        cursorVisible = self.flickerCountLeft <= self.settings.flickercount and not self.commandWin.enabled
        self.drawCursorLine(self.textOffset + (lineNrW, 0) + (w*(cx - ox), h*(cy - oy)), cursorVisible)

    def drawSelection(self, w, h, b, e, bx, by, lineNrW):
        """Draw a single selection rectangle"""
        ox, oy = self.displayOffset.t
        color = self.colors.selectionbg
        i = b
        while i < e:
            c = self.doc.text[i]
            # Can't deal with OSX line endings or word wrap (TODO !)
            if i == e - 1 or c == '\n':
                if oy <= by <= oy + self.textRange.h:
                    self.drawRect(color, self.textOffset + (lineNrW, 0) + (w*(bx - ox), h*(by - oy)), Size(w*(i + 1 - b), h))
                if i == e - 1:
                    return (bx + i + 1 - b, by)
                bx, by = 0, by + 1
                b = i # Mark the character no. of the selection beginning
            i += 1
        raise Exception('Character at end of selection not found')

    def drawText(self, text, labeling, lineNrW):
        """Draw the part of the text that should appear on the screen"""
        settings, colors = self.settings, self.colors
        w, h = settings.userfontsize.t # The size of one character
        i = self.displayIndex               # The index of the character currently being processed
        x, y = (0, 0)                       # The coordinates of that char (relative to screen)
        maxLength = len(self.doc.text)      # The amount of letters in a text (used as stop criterium)
        # The length of a linenumber - Can't deal with OSX line endings or word wrap (TODO !)
        while True:
            length = 0                      # The length of the interval currently being processed
            label = '' if not i in self.doc.labeling else self.doc.labeling[i]  # The current label

            # Draw a text interval with the same label
            # Can't deal with OSX line endings or word wrap (TODO !)
            while i < maxLength:
                tempLabel = '' if not i in self.doc.labeling else self.doc.labeling[i]
                if tempLabel != label or self.doc.text[i] == '\n':
                    break
                length += 1
                i += 1
            self.drawString(str(y + 1 + self.displayOffset.y), colors.linenumber, (lineNrW - settings.linenumbermargin, self.textOffset.y + h*y), 'ne')
            self.drawString(self.doc.text[i - length : i], colors.fromLabel(label), self.textOffset + (lineNrW + w*x, h*y))

            # Stop drawing at the end of the screen or the end of the text
            if h * y > self.size.h or i >= maxLength:
                break

            # Special case for the new line character - Can't deal with OSX line endings or word wrap (TODO !)
            if self.doc.text[i] == '\n':
                y += 1
                x = 0
                i += 1
            else:
                x += length

    def drawStatusWin(self, selectionstext):
        """Draw some stats to the bottom of the text win"""
        h = self.settings.statusheight
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

    def adjustWindow(self):
        """Adjust the window so that the cursor is in the allowed range"""
        (b, e) = self.oldSelection
        bx, by = self.getCoordFromChar(b).t
        ex, ey = self.getCoordFromChar(e, b, (bx, by)).t
        off = self.displayOffset
        # Vertical scrolling
        aim = off.y + self.settings.cursormargin.h
        if by < aim:
            off.y -= aim - by
            off.y = max(0, off.y)
            self.displayOffset = off
        aim = off.y + self.settings.cursormargin.h + self.cursorRange.h
        if ey > aim:
            off.y += ey - aim
            self.displayOffset = off
        # Horizontal scrolling
        # Todo

    def getTitle(self):
        return self.doc.filename + ('' if self.doc.saved else '*')

    def resetCursor(self):
        self.flickerCountLeft = self.settings.flickercount

    def calcLineNumberWidth(self, w):
        lineNumberWidth = 0
        if self.settings.linenumbers:
            lineNumberWidth = 2 * self.settings.linenumbermargin + w * self.nrOfLines
        return lineNumberWidth

    #
    # Win specific methods
    #
    def onKeyDown(self, c):
        if self.commandWin.enabled:
            self.commandWin.onKeyDown(c)

    def onMouseScroll(self, p, factor):
        maxLines = self.doc.text.count('\n') # Can't deal with OSX line endings or word wrap (TODO !)
        self.displayOffset = (self.displayOffset.x, min(maxLines, max(0, self.displayOffset.y + self.settings.scrolllines * factor)))
        if self.commandWin.enabled:
            self.commandWin.onMouseScroll(p, factor)

    def resize(self, draw=True):
        assert draw == False
        self.size = self.settings.size - (0, self.settings.tabsize.h)
        w, h = self.settings.userfontsize.t # The size of one character
        s = self.size - self.textOffset - (0, self.settings.statusheight if self.settings.statuswinenabled else 0)
        self.textRange = Size(s.w // w, s.h // h)
        self.commandWin.resize(False)

    def enable(self):
        Win.enable(self)
        self.resetCursor()

    #
    # Some helper methods
    #
    def getCoordFromChar(self, n, start=0, startPosTuple=(0, 0)):
        """Return (x, y) coordinates of the n-th character. This is a truly terrible method."""
        # Not a very fast method, especially because it's executed often and loops O(n) in the number of characters,
        # but then Chiel's datastructure for text will probably be changed and then this method has to be changed as well.
        x, y = startPosTuple
        text = self.doc.text
        for i in range(start, n):
            c = text[i]
            x += 1
            if c == '\n': # Can't deal with OSX line endings or word wrap (TODO !)
                y += 1
                x = 0
        return Pos(x, y)

    def getCharFromCoord(self, p):
        """Return character index from the (x, y) coordinates. This is a truly terrible method."""
        # Not a very fast method, especially because it's executed often and loops O(n) in the number of characters,
        # but then Chiel's datastructure for text will probably be changed and then this method has to be changed as well.
        i = 0
        w, h = self.settings.userfontsize.t
        offset = self.pos + self.textOffset
        x, y = p.t
        cx, cy = 0, 0
        text = self.doc.text
        try:
            while cy < y:
                c = text[i]
                if c == '\n': # Can't deal with OSX line endings or word wrap (TODO !)
                    cy += 1
                i += 1
            while cx < x:
                cx += 1
                c = text[i]
                if c == '\n':
                    return i
                i += 1
            return i
        except:
            return i

    def getCharFromPixelCoord(self, p):
        """Return character index from the (x, y) coordinates (in pixels). This is a truly terrible method."""
        # Not a very fast method, especially because it's executed often and loops O(n) in the number of characters,
        # but then Chiel's datastructure for text will probably be changed and then this method has to be changed as well.
        w, h = self.settings.userfontsize.t
        lineNrWidth = self.calcLineNumberWidth(w)
        offset = self.pos + self.textOffset + (lineNrWidth, 0)
        x, y = (p.x - offset.x) // w + self.displayOffset.x, (p.y - offset.y) // h + self.displayOffset.y
        return self.getCharFromCoord(Pos(x, y))

    #
    # Implement UserInterface methods
    #
    def touch(self):
        # This method is called from a different thread (the one fate runs in)
        self.redraw = True

    def notify(self, message):
        # This method is called from a different thread (the one fate runs in)
        raise NotImplementedError()

    def _getuserinput(self):
        # This method is called from a different thread (the one fate runs in)
        # Block untill you have something
        while not self.inputqueue:
            sleep(self.settings.fps_inv)
        return self.inputqueue.popleft()

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
        raise NotImplementedError()

