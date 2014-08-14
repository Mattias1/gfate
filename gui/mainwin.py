from .win import *
from .colors import *
from .textwin import TextWin
from .commandwin import CommandWin
from collections import deque
from PIL import Image, ImageTk


class MainWin(Win):
    """The main window class
    
    This is the main window for the gfate text editor.
    """

    def __init__(self, settings, app):
        Win.__init__(self, settings, app)

        self.selectedtab = -1 # Mark the tab that is selected while a mousekey is down
        self.queue = deque()

        self.textwins = []
        self.commandwin = CommandWin(settings, app)

        # self.addWin("First window.txt")
        # self.addWin("Second.txt")
        # self.addWin("Third.txt")
        # self.addWin("Fourth.txt")
        # self.enableTab(2)

        self.draw()

    def addWin(self, document):
        """Open a new file"""
        for win in self.textwins:
            win.disable()
        win = TextWin(self.settings, self.app, document)
        self.textwins.append(win)
        return win

    def enableTab(self, index):
        for win in self.textwins:
            win.disable()
        self.textwins[index].enable()

    def swapTabs(self, a, b):
        self.textwins[a], self.textwins[b] = self.textwins[b], self.textwins[a]

    def closeTab(self, index):
        win = self.textwins.pop(index)
        if win.enabled:
            if index < len(self.textwins):
                self.textwins[index].enable()
            elif self.textwins:
                self.textwins[index - 1].enable()
            else:
                self.quit()

    def draw(self):
        """Draw the main window"""
        # Draw myself
        self.fullClear()
        self.drawTabs()

        # Draw my active children
        for win in self.textwins:
            if win.enabled:
                win.draw()
        if self.commandwin.enabled:
            self.commandwin.draw()

    def onMouseDown(self, x, y, btnNr):
        # Hit tabs
        self.selectedtab = -1
        w, h = self.settings.tabwidth + self.settings.tabwidthextra, self.tabImg[0].height()
        if 3 <= y <= h:
            i = x // w
            if i < len(self.textwins):
                self.selectedtab = i

        if self.selectedtab > -1:
            if btnNr == 1:
                self.enableTab(i)
            elif btnNr == 2:
                self.closeTab(i)
            self.draw()

        # Pass the event on to all my children
        for win in self.textwins:
            if win.inside(x, y):
                win.onMouseDown(x, y, btnNr)
    def onMouseMove(self, x, y, btnNr):
        # Move the tabs
        i = x // (self.settings.tabwidth + self.settings.tabwidthextra)
        if i != self.selectedtab and btnNr == 1:
            if i < len(self.textwins):
                self.swapTabs(i, self.selectedtab)
                self.selectedtab = i
                self.draw()

        # Pass the event on to all my children
        for win in self.textwins:
            if win.inside(x, y):
                win.onMouseMove(x, y, btnNr)
    def onMouseUp(self, x, y, btnNr):
        # Deselect
        self.selectedtab = -1

        # Pass the event on to all my children
        for win in self.textwins:
            if win.inside(x, y):
                win.onMouseUp(x, y, btnNr)
    def onKeyDown(self, c):
        self.queue.append(c)
        self.draw()

    def resize(self, w=None, h=None, draw=True):
        """Override the resize window"""
        Win.resize(self, w, h, False)

        self.initTabs()

        try:
            for win in self.textwins:
                win.resize(w, h, False)
            self.commandwin.resize(w, h, False)
        except Exception:
            pass

        if draw:
            self.draw()

    def loop(self):
        """This method is being called every X miliseconds"""
        # Call my (active) children
        redraw = False
        for win in self.textwins:
            if win.enabled:
                redraw = win.loop()
        if self.commandwin.enabled:
            redraw = self.commandwin.loop() or redraw
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
            for nr in [2,5]:
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
            piltabs[nr] = piltabs[nr].resize((self.settings.tabwidth, h), Image.NEAREST)
        for y in range(h):
            pixs[6][0, y] = pixs[2][w - 1, y]
        piltabs[6] = piltabs[6].resize((self.width, h), Image.NEAREST)

        # Convert the images to Tk images
        self.tabImg = [self.loadImgTk(t) for t in piltabs]

    def drawTab(self, x, y, text, active=False):
        """Draw a single tab"""
        offset = 0 if active else 3
        w, h = self.tabImg[offset].width(), self.tabImg[offset].height()
        self.drawImg(x, y, self.tabImg[offset])
        self.drawImg(x + w, y, self.tabImg[1 + offset])
        self.drawImg(x + w + self.settings.tabwidth, y, self.tabImg[2 + offset])
        self.drawUIString(text, self.colors.tabtext, x + w + self.settings.tabwidth // 2, y + h // 2 + 2, "center")

    def drawTabs(self):
        """Manage the drawing of all the tabs"""
        y = self.settings.tabheight - self.tabImg[0].height()
        if y < 0:
            self.settings.tabheight = self.tabImg[0].height()
            y = 0
        # Draw tab background
        w = self.settings.tabwidth + self.settings.tabwidthextra
        self.drawRect(self.colors.tabbg, 0, 0, self.width, y + self.tabImg[0].height())
        activewin = -1
        # Draw inactive tabs
        for i, win in enumerate(self.textwins):
            if win.enabled:
                activewin = i
            else:
                self.drawTab(i * w, y, win.getTitle())
        # Draw tab bottom
        self.drawImg(0, y, self.tabImg[6])
        # Draw the active tab
        if activewin > -1:
            self.drawTab(activewin * w, y, self.textwins[activewin].getTitle(), True)
