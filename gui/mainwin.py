from .win import *
from .colors import *
from .textwin import TextWin
import fate
import fate.document
import fate.commands
from collections import deque


class MainWin(Win):
    """
    The main window class
    This is the main window for the gfate text editor.
    """

    def __init__(self, settings, app):
        Win.__init__(self, settings, app)

        self.selectedTab = -1 # Mark the tab that is selected while a mousekey is down

        self.textWins = []
        self.docList = fate.document.documentlist

    @property
    def activeWin(self):
        try:
            if fate.document.activedocument.ui:
                return fate.document.activedocument.ui
        except:
            return None

    @property
    def queue(self):
        return self.activeWin.inputqueue

    def addWin(self, doc):
        """Open a new file"""
        for win in self.textWins:
            win.disable()
        win = TextWin(self.settings, self.app, doc)
        self.textWins.append(win)
        return win

    def enableTab(self, newWin):
        for win in self.textWins:
            win.disable()
        newWin.enable()

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
        self.draw()

    def draw(self):
        """Draw the main window"""
        # Draw myself
        self.fullClear()
        self.drawTabs()

        # Draw my active child
        if self.activeWin != None:
            self.activeWin.draw()

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
                fate.commands.quit_document(self.docList[self.selectedTab])
            self.draw()

        # Pass the event on to my active child
        if self.activeWin and self.activeWin.inside(p):
            self.activeWin.onMouseDown(p, btnNr)
    def onMouseMove(self, p, btnNr):
        # Move the tabs
        i = p.x // (self.settings.tabsize.w + self.settings.tabwidthextra)
        if i != self.selectedTab and btnNr == 1:
            if i < len(self.textWins):
                self.swapTabs(i, self.selectedTab)
                self.selectedTab = i
                self.draw()

        # Pass the event on to my active child
        if self.activeWin.inside(p):
            self.activeWin.onMouseMove(p, btnNr)
    def onMouseUp(self, p, btnNr):
        # Deselect
        self.selectedTab = -1

        # Pass the event on to my active child
        if self.activeWin.inside(p):
            self.activeWin.onMouseUp(p, btnNr)

    def onKeyDown(self, c):
        if c == 'Ctrl-c':
            self.activeWin.notify('Ctrl-c is pressed, this is a gfate test message (mainWin.py - def onKeyDown).')
        if self.activeWin.acceptinput() and c:
            self.queue.append(c)
        self.activeWin.onKeyDown(c)
        self.draw()

    def resize(self, s=None, draw=True):
        """Override the resize window"""
        Win.resize(self, s, False)

        self.initTabs()

        try:
            for win in self.textWins:
                win.resize(s, False)
        except:
            pass

        if draw:
            self.draw()

    def loop(self):
        """This method is being called every n miliseconds (depending on the fps)"""
        # Call my active child
        if not self.activeWin:
            return False
        redraw = self.activeWin.loop()
        # Draw if nescessary
        if redraw:
            self.draw()
        # No redraw needed
        return False


    #
    # Tabs
    #
    def initTabs(self):
        """Create the images for the tabs"""
        # Load all images and their pixel maps
        tabr = self.loadImgPIL("tab.png")
        w, h = tabr.size
        piltabs = [Image.new("RGBA", tabr.size), Image.new("RGBA", (1, h)), tabr]
        for i in range(3):
            piltabs.append(piltabs[i].copy())
        piltabs.append(Image.new("RGBA", (1, h)))
        pixs = [t.load() for t in piltabs]

        # Paint the tabr images
        if tabr.mode == 'RGB' or tabr.mode == 'RGBA':
            for nr in [2, 5]:
                pixr = pixs[nr]
                tabColor = self.colors.toTuple(self.colors.bg if nr == 2 else self.colors.inactivetab)
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
            piltabs[nr] = piltabs[nr].resize((self.settings.tabsize.w, h), Image.NEAREST)
        for y in range(h):
            pixs[6][0, y] = pixs[2][w - 1, y]
        piltabs[6] = piltabs[6].resize((self.size.w, h), Image.NEAREST)

        # Convert the images to Tk images
        self.tabImgs = [self.loadImgTk(t) for t in piltabs]

    def drawTab(self, p, text, active=False):
        """Draw a single tab"""
        offset = 0 if active else 3
        w, h = self.tabImgs[offset].width(), self.tabImgs[offset].height()
        self.drawImg(p, self.tabImgs[offset])
        self.drawImg(p + (w, 0), self.tabImgs[1 + offset])
        self.drawImg(p + (w + self.settings.tabsize.w, 0), self.tabImgs[2 + offset])
        self.drawUIString(text, self.colors.tabtext, self.pos + p + (0, 9) + (self.settings.tabwidthextra, 0))

    def drawTabs(self):
        """Manage the drawing of all the tabs"""
        h = self.tabImgs[0].height()
        y = self.settings.tabsize.h - h
        if y < 0:
            self.settings.tabsize.h = h
            y = 0
        # Draw tab background
        w = self.settings.tabsize.w + self.settings.tabwidthextra
        self.drawRect(self.colors.tabbg, Pos(0, 0), Pos(self.size.w, y + h))
        activeWin = -1
        # Draw inactive tabs
        for i, win in enumerate(self.textWins):
            if win.enabled:
                activeWin = i
            else:
                self.drawTab(Pos(i * w, y), win.getTitle())
        # Draw tab bottom
        self.drawImg(Pos(0, y), self.tabImgs[6])
        # Draw the active tab
        if activeWin > -1:
            self.drawTab(Pos(activeWin * w, y), self.textWins[activeWin].getTitle(), True)

