from .win import *
from .colors import *
from .textwin import TextWin
import fate
import fate.document
from collections import deque
from PIL import Image, ImageTk, ImageDraw


class MainWin(Win):
    """The main window class

    This is the main window for the gfate text editor.
    """

    def __init__(self, settings, app):
        Win.__init__(self, settings, app)

        self.selectedtab = -1 # Mark the tab that is selected while a mousekey is down
        self.queue = deque()

        self.textwins = []

    @property
    def activewin(self):
        try:
            if fate.document.activedocument.ui:
                return fate.document.activedocument.ui
        except:
            return None

    def addWin(self, document):
        """Open a new file"""
        for win in self.textwins:
            win.disable()
        win = TextWin(self.settings, self.app, document)
        self.textwins.append(win)
        return win

    def enableTab(self, tab):
        for win in self.textwins:
            win.disable()
        try:
            self.textwins[tab].enable()
        except:
            tab.enable()

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

        # Draw my active child
        if self.activewin != None:
            self.activewin.draw()

    def onMouseDown(self, p, btnNr):
        # Hit tabs
        self.selectedtab = -1
        w, h = (self.settings.tabsize + (self.settings.tabwidthextra, 0)).t
        if 0 <= p.y <= h:
            i = p.x // w
            if i < len(self.textwins):
                # self.selectedtab = i
                self.queue.append(fate.document.goto_document(i))

        if self.selectedtab > -1:
            if btnNr == 1:
                self.enableTab(i)
            elif btnNr == 2:
                self.closeTab(i)
            self.draw()

        # Pass the event on to my active child
        if self.activewin.inside(p):
            self.activewin.onMouseDown(p, btnNr)
    def onMouseMove(self, p, btnNr):
        # Move the tabs
        i = p.x // (self.settings.tabsize.w + self.settings.tabwidthextra)
        if i != self.selectedtab and btnNr == 1:
            if i < len(self.textwins):
                self.swapTabs(i, self.selectedtab)
                self.selectedtab = i
                self.draw()

        # Pass the event on to my active child
        if self.activewin.inside(p):
            self.activewin.onMouseMove(p, btnNr)
    def onMouseUp(self, p, btnNr):
        # Deselect
        self.selectedtab = -1

        # Pass the event on to my active child
        if self.activewin.inside(p):
            self.activewin.onMouseUp(p, btnNr)
    def onKeyDown(self, c):
        if self.activewin.acceptinput() and c:
            self.queue.append(c)
        self.activewin.onKeyDown(c)
        self.draw()

    def resize(self, s=None, draw=True):
        """Override the resize window"""
        Win.resize(self, s, False)

        self.im = Image.new("RGBA", self.size.t)

        self.initTabs()

        try:
            for win in self.textwins:
                win.resize(s, False)
        except:
            pass

        if draw:
            self.draw()

    def loop(self):
        """This method is being called every X miliseconds"""
        # Call my active child
        redraw = self.activewin.loop()
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
        activewin = -1
        # Draw inactive tabs
        for i, win in enumerate(self.textwins):
            if win.enabled:
                activewin = i
            else:
                self.drawTab(Pos(i * w, y), win.getTitle())
        # Draw tab bottom
        self.drawImg(Pos(0, y), self.tabImgs[6])
        # Draw the active tab
        if activewin > -1:
            self.drawTab(Pos(activewin * w, y), self.textwins[activewin].getTitle(), True)
