"""
Module containing Win class.
The Win class is meant to hide some common interaction with the canvas
and provide some default or needed functionality for all window objects.
"""
from tkinter import *
from PIL import Image, ImageTk, ImageDraw
from .settings import *
from .colors import *


class Win:
    """Abstract window class"""

    def __init__(self, settings, app, pos):
        self.settings = settings
        self.colors = settings.colors
        self.enabled = True
        self.app = app
        self.g = app.canvas
        self.pos = pos
        self.size = Size(50, 50) # Should be set in the resize method

    def enable(self):
        """Enable this window."""
        self.enabled = True

    def disable(self):
        """Disable this window."""
        self.enabled = False

    def quit(self):
        """Quit the application"""
        self.app.quit()

    def containsPos(self, p):
        return self.pos.x <= p.x <= self.pos.x + self.size.w and self.pos.y <= p.y <= self.pos.y + self.size.h

    def onMouseDown(self, p, btnNr):
        pass
    def onMouseMove(self, p, btnNr):
        pass
    def onMouseUp(self, p, btnNr):
        pass
    def onKeyDown(self, c):
        pass
    def onMouseScroll(self, p, factor):
        pass
    def onMouseDownDouble(self, p, btnNr):
        pass
    def onMouseDownTriple(self, p, btnNr):
        pass

    def resize(self, draw=True):
        """Resize window."""
        pass

    def loop(self):
        """This method is being called every X miliseconds"""
        return False

    def draw(self):
        """This draw method needs to be overridden to draw the window content."""
        pass

    # Some draw methods to make sure all my subclasses don't have to bother about tkinters canvas
    def drawFString(self, text, c, p, font, anchor='nw'):
        self.g.create_text((self.pos + p).t, anchor=anchor, text=text, fill=c, font=font)
    def drawUIString(self, text, c, p, anchor='nw'):
        self.drawFString(text, c, p, self.settings.uifont, anchor=anchor)
    def drawString(self, text, c, p, anchor='nw'):
        self.drawFString(text, c, p, self.settings.userfont, anchor=anchor)

    def drawLine(self, c, p, q, w=1):
        self.g.create_line((self.pos + p).t, (self.pos + q).t, fill=c)
        # TODO: Use width
    def drawHorizontalLine(self, c, h, w=1):
        self.drawLine(c, Pos(0, h), Pos(self.size.w, h), w)

    def drawRect(self, c, p, s):
        self.drawRectBorder(c, p, s, 0)
    def drawRectBorder(self, c, p, s, borderw=1):
        self.g.create_rectangle((self.pos + p).t, (self.pos + p + s).t, fill=c, width=borderw)

    def loadImgPIL(self, path):
        return Image.open('img/' + path)
    def loadImgTk(self, img):
        return ImageTk.PhotoImage(img)
    def loadImg(self, path):
        return self.loadImgTk(self.loadImgPIL(path))

    def drawImg(self, p, img, anchor='nw'):
        self.g.create_image((self.pos + p).t, image=img, anchor=anchor)

    def fullClear(self):
        self.g.delete(ALL)
        self.clear(self.colors.bg)
    def clear(self, c):
        self.drawRect(c, Pos(0, 0), self.size)

    def drawCursorLine(self, p, cursorvisible):
        if cursorvisible:
            self.drawLine(self.colors.text, p, p + (0, self.settings.userfontsize.h))

