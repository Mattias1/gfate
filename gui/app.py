import os
from tkinter import *
from tkinter.ttk import *
from mattycontrols.MattyControls import *
from .mainwin import MainWin
from .settings import Settings, Pos, Size
from .options import Options


class Application(Frame):
    def __init__(self, settings, master, rootpath):
        """The tkinter frame that manages the canvas and the keyboard and mouse interaction"""
        frame_init(self, master)
        master.title('fate - test')
        self.rootpath = rootpath

        self.ctrl, self.shift, self.alt, self.superkey = False, False, False, False

        self.canvas = Cnvs(master, bd=-2)
        self.master.wm_protocol("WM_DELETE_WINDOW", self.quitApp)
        self.canvas.bind('<Button>', self.onMouseDown)
        self.canvas.bind('<Double-Button>', self.onMouseDownDouble)
        self.canvas.bind('<Triple-Button>', self.onMouseDownTriple)
        self.canvas.bind('<Motion>', self.createOnMouseMove(0))
        self.canvas.bind('<B1-Motion>', self.createOnMouseMove(1))
        self.canvas.bind('<B2-Motion>', self.createOnMouseMove(2))
        self.canvas.bind('<B3-Motion>', self.createOnMouseMove(3))
        self.canvas.bind('<MouseWheel>', self.onMouseScroll)
        self.canvas.bind('<4>', self.onMouseScroll)
        self.canvas.bind('<5>', self.onMouseScroll)
        self.canvas.bind('<ButtonRelease>', self.onMouseUp)
        self.master.bind('<Key>', self.onKeyDown)
        self.master.bind('<KeyRelease>', self.onKeyUp)
        self.resize_bind_id = self.master.bind('<Configure>', self.onResizeMoveFocus)
        self.canvas.highlightthickness = 0
        self.canvas.width = settings.size.w
        self.canvas.height = settings.size.h
        self.canvas.locateInside(self, d=0)

        self.mainWindow = MainWin(settings, self)
        self.mainWindow.resize(True)

        self.mainWindow.setIcon('favicon.ico')

        self.optionsWindow = None

        self.settings = settings

        self.master.after(int(self.settings.fps_inv * 1000), self.loop)
        self.fateThread = None

    def quitApp(self):
        self.mainWindow.quit()

    def onMouseDown(self, event):
        self.mainWindow.onMouseDown(Pos(event.x, event.y), event.num)
    def onMouseDownDouble(self, event):
        self.mainWindow.onMouseDownDouble(Pos(event.x, event.y), event.num)
    def onMouseDownTriple(self, event):
        self.mainWindow.onMouseDownTriple(Pos(event.x, event.y), event.num)

    def createOnMouseMove(self, btnNr):
        return lambda event: self.mainWindow.onMouseMove(Pos(event.x, event.y), btnNr)

    def onMouseScroll(self, event):
        # respond to Linux or Windows wheel event
        factor = 0
        if event.num == 5 or event.delta == -120:
            factor = 1
        if event.num == 4 or event.delta == 120:
            factor = -1
        self.mainWindow.onMouseScroll(Pos(event.x, event.y), factor)

    def onMouseUp(self, event):
        self.mainWindow.onMouseUp(Pos(event.x, event.y), event.num)

    def onKeyDown(self, event):
        if self.setModifyKeys(event, True):
            self.mainWindow.onKeyDown(self.getchar(event))

    def onKeyUp(self, event):
        self.setModifyKeys(event, False)

    def setModifyKeys(self, event, value):
        # Set the modify keys and return whether or not something has to be done still.
        if event.keysym_num in {65505, 65506}:
            self.shift = value
        elif event.keysym_num in {65507, 65508}:
            self.ctrl = value
        elif event.keysym_num in {65513, 65514}:
            self.alt = value
        elif event.keysym_num in {65371, 65372, 65515, 65516}:
            self.superkey = value
        else:
            return True
        return False

    def onResizeMoveFocus(self, event):
        # Don't handle event when the options window is open.
        if self.optionsWindow:
            return

        # On focus
        self.ctrl, self.shift, self.alt, self.superkey = False, False, False, False

        # On resize
        s = Size(event.width, event.height)
        if s != self.settings.size:
            self.settings.size = s
            self.canvas.width, self.canvas.height = s.w, s.h
            self.mainWindow.resize()

    def loop(self):
        """Private method to manage the loop method"""
        self.mainWindow.loop()
        if not self.fateThread.isAlive() and self.mainWindow.activeWin:
            # If fate crashed, close gfate but keep the console open for just a bit
            self.master.quit()
            self.quitOnFateError = True
        else:
            self.master.after(int(self.settings.fps_inv * 1000), self.loop)

    def getchar(self, e):
        """Convert a tkinter event (given these three different representations of the same char)"""
        # Get prefixes
        prefix = ('ctrl-' if self.ctrl else '') + ('alt-' if self.alt else '') + ('super-' if self.superkey else '')

        # Some basic key mapping
        num = e.keysym_num
        name = e.keysym
        if 31 < num < 256:
            c = chr(num)
        else:
            c = name

        # Some exceptopns
        if num == 65307: c = 'esc'
        elif num == 65288: c = '\b'
        elif num == 65293: c = '\n'
        elif num == 65289: c = 'backtab' if self.shift else '\t'
        elif num == 65549: c = 'capslock'

        # Name the F-keys to 'F(#)', not sure why though (e.keysym gives me F1 - F12).
        if 65470 <= num <= 65481:
            c = 'f{}'.format(num - 65469)

        return prefix + c

    def showOptions(self):
        # self.optionsWindow = Options(self.master, self, self.settings)
        # print('AFTER OPTIONS')
        pass
