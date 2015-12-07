import os
from .win import *
from .colors import *
from .textwin import TextWin
import fate
import fate.document
from fate.pointer import PointerClick, PointerDoubleClick, PointerTripleClick, PointerInput
from collections import deque


class MainWin(Win):
    """
    The main window class
    This is the main window for the gfate text editor.
    """

    def __init__(self, settings, app):
        Win.__init__(self, settings, app, Pos(0, 0))

        self.selectedTab = -1       # Mark the tab that is selected while a mousekey is down
        self.selectedScrollbar = -1 # Mark the scrollbar that is selected while a mousekey is down (1=vert, 2=hor)
        self.tabImgs = None
        self.scrollImgs = None
        self.scrollImgsPil = None
        self.gearImg = None
        self.mouseDownStartPos = Pos(-1, -1)
        self.redrawMarker = False
        self.updatedScrollImages = False

        self.textWins = []
        self.docList = fate.document.documentlist

    @property
    def activeWin(self):
        try:
            if fate.document.activedocument.ui.win:
                return fate.document.activedocument.ui.win
        except:
            return None

    @property
    def queue(self):
        return self.activeWin.api.inputqueue

    def addWin(self, doc):
        """Open a new file"""
        for win in self.textWins:
            win.disable()
        win = TextWin(self.settings, self.app, doc)
        self.textWins.append(win)
        win.resize(False)
        return win.api

    def enableTab(self, newWin):
        for win in self.textWins:
            win.disable()
        newWin.enable()
        self.updateScrollImgs()
        self.redraw()
        newWin.loop()

    def swapTabs(self, a, b):
        self.textWins[a], self.textWins[b] = self.textWins[b], self.textWins[a]
        self.docList[a], self.docList[b] = self.docList[b], self.docList[a]

    def closeTab(self, index):
        win = self.textWins.pop(index)
        if win.enabled:
            if index < len(self.textWins):
                self.textWins[index].enable()
            elif self.textWins:
                self.textWins[index - 1].enable()
            else:
                self.app.master.quit()
                return
        self.redraw()

    def redraw(self):
        """Mark the window for redrawing"""
        self.redrawMarker = True

    def draw(self):
        """Draw the main window"""
        # Draw myself
        self.fullClear()
        self.drawTabs()

        # Draw my active child
        if self.activeWin != None:
            self.activeWin.draw()

    def scrollbarClicks(self, p):
        # Manage scrollbar clicks
        vert, hor = self.settings.scrollbars in {'both', 'vertical'}, self.settings.scrollbars in {'both', 'horizontal'}
        barW = self.settings.scrollbarwidth
        if vert:
            x, y = self.activeWin.pos.x + self.activeWin.size.w, self.activeWin.pos.y
            h = self.activeWin.size.h
            # Check if the user clicked somewhere in the (vertical) scrollbar region
            if x <= p.x <= x + barW and y <= p.y <= y + h:
                # The up button
                if p.y <= y + barW:
                    self.activeWin.scrollText(True, -1)
                # The scrollbar (todo: split in two)
                elif p.y <= y + h - barW:
                    posY = self.activeWin.calcScrollbarPos(True) + self.activeWin.pos.y
                    if p.y < posY:
                        self.queue.append(fate.commands.movepageup)
                    elif p.y > posY + self.scrollImgs[2].height() + 2 * self.scrollImgs[2].width():
                        self.queue.append(fate.commands.movepagedown)
                    else:
                        print('todo: drag')
                        self.selectedScrollbar = 1
                # The down button
                else:
                    self.activeWin.scrollText(True, 1)
                self.draw()
        if hor:
            x, y = self.activeWin.pos.x, self.activeWin.pos.y + self.activeWin.size.h
            w = self.activeWin.size.w
            # Check if the user clicked somewhere in the (horizontal) scrollbar region
            if x <= p.x <= x + w and y <= p.y <= y + barW:
                # The left button
                if p.x <= x + barW:
                    self.activeWin.scrollText(False, -1)
                # The scrollbar (todo: split in two)
                elif p.x <= x + w - barW:
                    self.selectedScrollbar = 2
                # The right button
                else:
                    self.activeWin.scrollText(False, 1)
                self.draw()

    def onMouseDown(self, p, btnNr):
        # Hit tabs
        self.selectedTab = -1
        w, h = (self.settings.tabsize + (self.settings.tabwidthextra, 0)).t
        if 0 <= p.y <= h:
            i = p.x // w
            if i < len(self.textWins):
                self.selectedTab = i

        if self.selectedTab > -1:
            if btnNr == 1:
                self.queue.append(fate.document.goto_document(i))
            elif btnNr == 2:
                self.queue.append(fate.commands.quit_document(self.docList[self.selectedTab]))
            self.draw()

        # Hit the gear (options button)
        if btnNr == 1 and self.size.w - h < p.x < self.size.w and 0 < p.y < h:
            self.app.showOptions()

        # Hit scrollbar button
        if btnNr == 1:
            self.scrollbarClicks(p)

        # Forward click to children
        if self.activeWin and self.activeWin.containsPos(p):
            # Store position of the click (or maybe drag?)
            self.mouseDownStartPos = p
            # Pass the event on to my active child
            self.activeWin.onMouseDown(p, btnNr)
    def onMouseDownDouble(self, p, btnNr):
        # Forward double click
        if btnNr == 1 and self.activeWin and self.activeWin.containsPos(p):
            b = self.activeWin.getCharFromPixelCoord(p)
            self.queue.append(PointerDoubleClick(b))
        # Check scrollbar (you want to be able to click it multiple times close after eachother)
        elif btnNr == 1:
            self.scrollbarClicks(p)
    def onMouseDownTriple(self, p, btnNr):
        # Forward triple click
        if btnNr == 1 and self.activeWin and self.activeWin.containsPos(p):
            b = self.activeWin.getCharFromPixelCoord(p)
            self.queue.append(PointerTripleClick(b))
        # Check scrollbar (you want to be able to click it multiple times close after eachother)
        elif btnNr == 1:
            self.scrollbarClicks(p)
    def onMouseMove(self, p, btnNr):
        # Move the tabs
        i = p.x // (self.settings.tabsize.w + self.settings.tabwidthextra)
        if self.selectedTab != -1 and i != self.selectedTab and btnNr == 1:
            if i < len(self.textWins):
                self.swapTabs(i, self.selectedTab)
                self.selectedTab = i
                self.redraw()

        # Move the scrollbar
        # TODO...
        # SOMETHING WITH TEXTWIN . SCROLLWINDOW or something

        # Pass the event on to my active child
        if self.activeWin.containsPos(p):
            self.activeWin.onMouseMove(p, btnNr)
    def onMouseScroll(self, p, factor):
        # Pass the event on to my active child
        if self.activeWin.containsPos(p, False, False):
            self.activeWin.onMouseScroll(p, factor, not self.app.shift)
            self.redraw()
        # So we are not in the window without scrollbars, but we are in the window with horizontal scrollbar
        elif self.activeWin.containsPos(p, False, True):
            self.activeWin.onMouseScroll(p, factor, False)
            self.redraw()
        # So we are not in the normal window or with horizontal scrollbar, but we are in the window with vertical scrollbar
        elif self.activeWin.containsPos(p, True, False):
            self.activeWin.onMouseScroll(p, factor, True)
            self.redraw()
    def onMouseUp(self, p, btnNr):
        # Deselect
        self.selectedTab = -1
        self.selectedScrollbar = -1

        # Fire final mouse event
        if self.mouseDownStartPos != (-1, -1):
            e = self.activeWin.getCharFromPixelCoord(p)
            if self.mouseDownStartPos == p:
                self.queue.append(PointerClick(e))
            else:
                b = self.activeWin.getCharFromPixelCoord(self.mouseDownStartPos)
                self.queue.append(PointerInput(b, e-b))
            self.mouseDownStartPos = Pos(-1, -1)

        # Pass the event on to my active child
        if self.activeWin.containsPos(p):
            self.activeWin.onMouseUp(p, btnNr)

    def onKeyDown(self, c):
        if c:
            self.queue.append(c)
        self.activeWin.onKeyDown(c)

    def quit(self):
        """Quit the entire application"""
        inputQueue = self.queue
        fate.commands.force_quit()
        inputQueue.append('Cancel') # Stop the input thread from running

    def resize(self, redraw=True):
        """Override the resize window"""
        self.size = self.settings.size

        for win in self.textWins:
            win.resize(False)

        self.initMiscImgs()
        self.initTabImgs()
        self.initScrollImgs()

        if redraw:
            self.redraw()

    def loop(self):
        """This method is being called every n miliseconds (depending on the fps)"""
        # Call my active child
        if not self.activeWin:
            return False
        self.activeWin.loop()
        # Draw if nescessary
        if self.redrawMarker:
            self.draw()
            self.redrawMarker = False


    #
    # Misc images
    #
    def initMiscImgs(self):
        """Create some misc images (settings gear)"""
        pilImgs = [self.loadImgPIL(url) for url in ['gear.png']]
        pixs = [t.load() for t in pilImgs]

        # Paint the scroll images
        for i, img, pix in [(i, pilImgs[i], pixs[i]) for i in [0]]:
            if img.mode in ['RGB', 'RGBA']:
                w, h = img.size
                color = self.colors.toTuple(self.colors.gear)
                diff = [color[i] - pix[4, h // 2][i] for i in range(3)]
                temp = []
                for y in range(h):
                    for x in range(w):
                        temp = [min(255, max(0, pix[x, y][i] + diff[i])) for i in range(3)]
                        temp.append(pix[x, y][3])
                        pix[x, y] = tuple(temp)

        # Convert the images to Tk images
        self.gearImg = self.loadImgTk(pilImgs[0])


    #
    # Tab images
    #
    def initTabImgs(self):
        """Create the images for the tabs"""
        # Load all images and their pixel maps
        tabr = self.loadImgPIL('tab.png')
        w, h = tabr.size
        pilTabs = [Image.new('RGBA', tabr.size), Image.new('RGBA', (1, h)), tabr]
        pilTabs.extend([pilTabs[i].copy() for i in [0, 1, 2, 1]])
        pixs = [t.load() for t in pilTabs]

        # Paint the tabr images
        if tabr.mode in ['RGB', 'RGBA']:
            for nr in [2, 5]:
                pixr = pixs[nr]
                tabColor = self.colors.toTuple(self.colors.activetabbg if nr == 2 else self.colors.inactivetabbg)
                diff = [tabColor[i] - pixr[0, h-1][i] for i in range(3)]
                temp = []
                for y in range(h):
                    for x in range(w):
                        temp = [min(255, max(0, pixr[x, y][i] + diff[i])) for i in range(3)]
                        temp.append(pixr[x, y][3])
                        pixr[x, y] = tuple(temp)

        # Create the tabl images
        for nr in [0, 3]:
            pixl, pixr = pixs[nr], pixs[nr + 2]
            for y in range(h):
                for x in range(w):
                    pixl[x, y] = pixr[w - 1 - x, y]

        # Create the tabc and tabbg images
        for nr in [1, 4]:
            pixc, pixr = pixs[nr], pixs[nr + 1]
            for y in range(h):
                pixc[0, y] = pixr[0, y]
            pilTabs[nr] = pilTabs[nr].resize((self.settings.tabsize.w, h), Image.NEAREST)
        for y in range(h):
            pixs[6][0, y] = pixs[2][w - 1, y]
        pilTabs[6] = pilTabs[6].resize((self.size.w, h), Image.NEAREST)

        # Convert the images to Tk images
        self.tabImgs = [self.loadImgTk(img) for img in pilTabs]

    def drawTab(self, p, text, active=False):
        """Draw a single tab"""
        offset = 0 if active else 3
        w, h = self.tabImgs[offset].width(), self.tabImgs[offset].height()
        self.drawImg(p, self.tabImgs[offset])
        self.drawImg(p + (w, 0), self.tabImgs[1 + offset])
        self.drawImg(p + (w + self.settings.tabsize.w, 0), self.tabImgs[2 + offset])
        self.drawUIString(text, self.colors.activetab if active else self.colors.inactivetab,
            self.pos + p + (0, 9) + (self.settings.tabwidthextra, 0))

    def drawTabs(self):
        """Manage the drawing of all the tabs"""
        h = self.tabImgs[0].height()
        y = self.settings.tabsize.h - h
        if y < 0:
            self.settings.tabsize.h = h
            y = 0
        # How to handle file names
        tabname = lambda name: name
        if self.settings.tabname == 'filename':
            tabname = lambda name: os.path.basename(name)
        # Draw tab background
        w = self.settings.tabsize.w + self.settings.tabwidthextra
        self.drawRect(self.colors.headerbg, Pos(0, 0), Pos(self.size.w, y + h))
        activeWin = -1
        # Draw inactive tabs
        for i, win in enumerate(self.textWins):
            if win.enabled:
                activeWin = i
            else:
                self.drawTab(Pos(i * w, y), tabname(win.getTitle()))
        # Draw tab bottom
        self.drawImg(Pos(0, y), self.tabImgs[6])
        # Draw the active tab
        if activeWin > -1:
            self.drawTab(Pos(activeWin * w, y), tabname(self.textWins[activeWin].getTitle()), True)

        # Draw options gear
        gearOffset = 5
        self.drawImg(Pos(self.size.w - self.gearImg.width() - gearOffset, gearOffset), self.gearImg)

    #
    # Scroll images
    #
    def initScrollImgs(self):
        """Create the images for the scroll bars and buttons"""
        # Load all images and their pixel maps [bg, top, middle, bottom, bg, left, middle, right, up, right, down, left]
        pilImgs = [self.loadImgPIL(url) for url in ['scrollbg.png', 'scrolltop.png', 'scrollup.png']]
        self.settings.scrollbarwidth = pilImgs[0].size[0]
        w, h = pilImgs[1].size
        sq = Image.new('RGBA', (w, h))
        pilImgs[2:2] = [Image.new('RGBA', (w, 1)), sq, Image.new('RGBA', (1, self.settings.scrollbarwidth)), sq.copy(), Image.new('RGBA', (1, h)), sq.copy()]
        pilImgs.extend([sq.copy(), sq.copy(), sq.copy()])
        pixs = [t.load() for t in pilImgs]
        pixBgV, pixTop, pixMidV, pixBottom, pixBgH, pixLeft, pixMidH, pixRight, pixN, pixE, pixS, pixW = pixs

        # Paint the scroll images
        for img, pix in [(pilImgs[i], pixs[i]) for i in [1, 8]]:
            if img.mode in ['RGB', 'RGBA']:
                color = self.colors.toTuple(self.colors.scroll)
                diff = [color[i] - pix[w // 2, h // 2][i] for i in range(3)]
                temp = []
                for y in range(h):
                    for x in range(w):
                        temp = [min(255, max(0, pix[x, y][i] + diff[i])) for i in range(3)]
                        temp.append(pix[x, y][3])
                        pix[x, y] = tuple(temp)
        # Paint the background image
        if pilImgs[0].mode in ['RGB', 'RGBA']:
            color = self.colors.toTuple(self.colors.scrollbg)
            diff = [color[i] - pixBgV[0, 0][i] for i in range(3)]
            temp = []
            for x in range(self.settings.scrollbarwidth):
                temp = [min(255, max(0, pixBgV[x, 0][i] + diff[i])) for i in range(3)]
                if pilImgs[0].mode == 'RGBA':
                    temp.append(pixBgV[x, y][3])
                pixBgV[x, 0] = tuple(temp)

        # Create scroll bottom, right and left images
        for y in range(h):
            for x in range(w):
                pixBottom[x, y] = pixTop[x, h - 1 - y]
                pixLeft[x, y] = pixTop[y, x]
                pixRight[x, y] = pixTop[h - 1 - y, w - 1 - x]

        # Create the middle and bg images
        for i in range(self.settings.scrollbarwidth):
            pixBgH[0, i] = pixBgV[i, 0]
        for i in range(w):
            pixMidV[i, 0] = pixBottom[i, 0]
            pixMidH[0, i] = pixRight[0, i]
        otherBarExtra = self.settings.scrollbarwidth if self.settings.scrollbars == 'both' else 0
        statusExtra = self.settings.statusheight if self.settings.statuswinenabled else 0
        pilImgs[0] = pilImgs[0].resize((self.settings.scrollbarwidth, self.settings.size.h - self.settings.tabsize.h - otherBarExtra - statusExtra), Image.NEAREST)
        pilImgs[4] = pilImgs[4].resize((self.settings.size.w - otherBarExtra, self.settings.scrollbarwidth), Image.NEAREST)
        self.scrollImgsPil = [pilImgs[i] for i in [2, 6]]
        self.updateScrollImgs()

        # Create the E, S, W images
        for y in range(h):
            for x in range(w):
                pixE[x, y] = pixN[h - 1 - y, w - 1 - x]
                pixS[x, y] = pixN[x, h - 1 - y]
                pixW[x, y] = pixN[y, x]

        # Convert the images to Tk images and save the original for the middle images
        self.scrollImgs = [self.loadImgTk(img) for img in pilImgs]

    def updateScrollImgs(self):
        """Update the images for the moving part of the scroll bars"""
        # Resize the middle images (2 and 6 in [bg, top, middle, bottom, bg, left, middle, right, up, right, down, left])
        w = self.scrollImgsPil[0].size[0]
        win = self.activeWin
        if not win:
            return
        h1 = win.size.h * win.textRange.h // (win.textRange.h + win.nrOfLines)
        h2 = win.size.w * win.textRange.w // (win.textRange.w + 50) # TODO: use self.maxNrOfCharsOnALine
        h1, h2 = [max(self.settings.minimumscrollbarsize, h) for h in [h1, h2]]
        self.scrollImgsPil[0] = self.scrollImgsPil[0].resize((w, h1), Image.NEAREST)
        self.scrollImgsPil[1] = self.scrollImgsPil[1].resize((h2, w), Image.NEAREST)
        self.updatedScrollImages = True

