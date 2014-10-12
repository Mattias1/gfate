from .win import *
from .commandwin import CommandWin
from .statuswin import StatusWin
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
        self.statusWin = StatusWin(settings, app, doc, self)
        self.doc = doc
        self.doc.OnQuit.add(self.onQuit)
        self.doc.OnActivate.add(self.onActivate)
        self.flickerCountLeft = 0
        self.redraw = False
        self.oldSelection = self.doc.selection[-1]
        self.textOffset = Pos(6, 4)     # Margin for the text in px (so that it doesn't hug the borders)
        self.displayOffset = Pos(0, 0)  # The character with this pos (col, row) is the first one to be drawn (so it's in the top left of the text win)
        self.displayIndex = 0           # The index of the above character in the self.doc.text string
        self.textRange = Size(0, 0)     # The amount of letters that fit in the screen
        self.nrOfLines = 0              # The total number of lines (ie. newline chars) in self.doc.text

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
            self.nrOfLines = self.doc.text.count('\n')
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

        # Draw scrollbars
        self.drawScrollbars()

        # Draw statuswin
        if self.settings.statuswinenabled:
            self.statusWin.draw(selectionstext)

        # Draw commandWin
        if self.commandWin.enabled:
            self.commandWin.draw()

    def drawCursor(self, cx, cy, lineNrW):
        """Draw a single cursor (that is, an empty selection)"""
        ox, oy = self.displayOffset.t
        if not oy <= cy <= oy + self.textRange.h:
            return
        w, h = self.settings.userfontsize.t
        cursorVisible = self.flickerCountLeft <= self.settings.flickercount and not self.commandWin.enabled and cx >= ox
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
                    fromX = w*(bx - ox)
                    width = w*(i + 1 - b)
                    if fromX < 0:
                        width += fromX
                        fromX = 0
                    if width > 0:
                        self.drawRect(color, self.textOffset + (lineNrW, 0) + (fromX, h*(by - oy)), Size(width, h))
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
                # Now skip the first "displayOffset.x'th" characters (except with newline chars)
                for j in range(self.displayOffset.x + 1):
                    i += 1
                    if i == maxLength or self.doc.text[i] == '\n':
                        break
            else:
                x += length

    def drawScrollbars(self):
        """Draw the scroll bars"""
        # [bg, top, middle, bottom, bg, left, middle, right, up, right, down, left]           
        scrollImgs = self.app.mainWindow.scrollImgs
        imgBgV, imgTop, imgMidV, imgBottom, imgBgH, imgLeft, imgMidH, imgRight, imgN, imgE, imgS, imgW = scrollImgs
        vert, hor = self.settings.scrollbars in {'both', 'vertical'}, self.settings.scrollbars in {'both', 'horizontal'}
        barW = imgTop.width()
        padding = (self.settings.scrollbarwidth - barW) // 2
        x, y = self.size.w + padding, self.size.h + padding
        w, h = x - 5 * padding - 2 * barW, y - 3 * padding - 2 * barW
        ratio = 0

        # Draw vertical scrollbar
        if vert:
            if self.nrOfLines > 0:
                ratio = self.displayOffset.y / self.nrOfLines
            posY = int(ratio * (h - imgMidV.height() - 2 * barW)) + barW + padding
            # Background
            self.drawRect(self.colors.scrollbg, Pos(x - padding, 0), Size(imgBgV.width(), imgBgV.height()))
            self.drawImg(Pos(x - padding, 0), imgBgV)
            # Arrows
            self.drawImg(Pos(x, padding), imgN)
            self.drawImg(Pos(x, y - 2 * padding - barW), imgS)
            # The scrollbar
            self.drawImg(Pos(x, posY), imgTop)
            self.drawImg(Pos(x, posY + barW), imgMidV)
            self.drawImg(Pos(x, posY + barW + imgMidV.height()), imgBottom)
        # Draw horizontal scrollbar
        if hor:
            # if self.nrOfLines > 0:
            ratio = self.displayOffset.x / 50 # self.nrOfLines # TODO: use self.maxNrOfCharsOnALine
            posX = int(ratio * (w - imgMidH.width() - 2 * barW)) + barW + padding
            # Background
            self.drawRect(self.colors.scrollbg, Pos(0, y - padding), Size(imgBgH.width(), imgBgH.height()))
            self.drawImg(Pos(0, y - padding), imgBgH)
            # Arrows
            self.drawImg(Pos(padding, y), imgW)
            self.drawImg(Pos(x - 3 * padding - barW, y), imgE)
            # The scrollbar
            self.drawImg(Pos(posX, y), imgLeft)
            self.drawImg(Pos(posX + barW, y), imgMidH)
            self.drawImg(Pos(posX + barW + imgMidH.width(), y), imgRight)

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
        # TODO ...

    def scrollText(self, vert, n):
        # Scroll a window vertically (or horizontally if vert is False) down n chars
        if vert:
            maxLines = self.doc.text.count('\n') # Can't deal with OSX line endings or word wrap (TODO !)
            self.displayOffset = (self.displayOffset.x, min(maxLines, max(0, self.displayOffset.y + n)))
        else:
            maxChars = 50 # TODO: vertical scroll check?
            self.displayOffset = (min(maxChars, max(0, self.displayOffset.x + n)), self.displayOffset.y)

    def getTitle(self):
        return self.doc.filename + ('' if self.doc.saved else '*')

    def resetCursor(self):
        self.flickerCountLeft = self.settings.flickercount

    def calcLineNumberWidth(self, w):
        lineNumberWidth = 0
        if self.settings.linenumbers:
            lineNumberWidth = 2 * self.settings.linenumbermargin + w * len(str(self.nrOfLines))
        return lineNumberWidth

    def containsPos(self, p, includeVerticalScroll = False, includeHorizontalScroll = False):
        extra = Size(0, 0)
        if includeVerticalScroll:
            extra.w += self.settings.scrollbarwidth
        if includeHorizontalScroll:
            extra.h += self.settings.scrollbarwidth
        return self.pos.x <= p.x <= self.pos.x + self.size.w + extra.w and self.pos.y <= p.y <= self.pos.y + self.size.h + extra.h

    #
    # Win specific methods
    #
    def onKeyDown(self, c):
        if self.commandWin.enabled:
            self.commandWin.onKeyDown(c)

    def onMouseScroll(self, p, factor, scrollVertical = True):
        self.scrollText(scrollVertical, self.settings.scrolllines * factor)
        if self.commandWin.enabled:
            self.commandWin.onMouseScroll(p, factor)

    def resize(self, draw=True):
        assert draw == False
        vert, hor = self.settings.scrollbars in {'both', 'vertical'}, self.settings.scrollbars in {'both', 'horizontal'}
        scrollSize = Size(self.settings.scrollbarwidth if vert else 0, self.settings.scrollbarwidth if hor else 0)
        statusSize = (0, self.settings.statusheight if self.settings.statuswinenabled else 0)
        self.size = self.settings.size - (0, self.settings.tabsize.h) - scrollSize - statusSize
        w, h = self.settings.userfontsize.t # The size of one character
        s = self.size - self.textOffset
        self.textRange = Size(s.w // w, s.h // h)
        self.commandWin.resize(False)
        self.statusWin.resize(False)

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

