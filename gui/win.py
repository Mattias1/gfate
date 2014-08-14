"""
Module containing Win class.
The Win class is meant to hide some common interaction with curses.
"""
from tkinter import *
from PIL import Image, ImageTk
from .settings import *
from .colors import *


class Win:
    """Abstract window class"""

    def __init__(self, settings, app, width=None, height=None, x=0, y=0):
        self.settings = settings
        self.colors = settings.colors
        self.enabled = True
        self.app = app
        self.g = app.canvas
        self.x, self.y = x, y
        self.resize(width, height, False)

    def enable(self):
        """Enable this window."""
        self.enabled = True

    def disable(self):
        """Disable this window."""
        self.enabled = False

    def quit(self):
        """Quit the application"""
        self.app.quit()

    def inside(self, x, y):
        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height

    def onMouseDown(self, x, y, btnNr):
        pass
    def onMouseMove(self, x, y, btnNr):
        pass
    def onMouseUp(self, x, y, btnNr):
        pass
    def onKeyDown(self, c):
        pass

    def resize(self, w=None, h=None, draw=True):
        """Resize window."""
        if w == None:
            w = self.settings.width
        if h == None:
            h = self.settings.height
        self.width, self.height = w, h
        if draw:
            self.draw()

    def loop(self):
        """This method is being called every X miliseconds"""
        return False

    def draw(self):
        """This draw method needs to be overridden to draw the window content."""
        pass

    # Some draw methods to make sure all my subclasses don't have to bother about tkinters canvas
    def drawFString(self, text, c, x, y, font, anchor="nw"):
        self.g.create_text(self.x+x, self.y+y, anchor=anchor, text=text, fill=c, font=font)
    def drawUIString(self, text, c, x, y, anchor="nw"):
        self.drawFString(text, c, x, y, self.settings.uifont, anchor=anchor)
    def drawString(self, text, c, x, y, anchor="nw"):
        self.drawFString(text, c, x, y, self.settings.userfont, anchor=anchor)

    def drawLine(self, c, x, y, p, q, w=1):
        self.g.create_line(self.x+x, self.y+y, self.x+p, self.y+q, fill=c) # Todo: use the line width

    def drawRect(self, c, x, y, w, h):
        self.drawRectBorder(c, x, y, w, h, 0)
    def drawRectBorder(self, c, x, y, w, h, borderw=1):
        self.g.create_rectangle(self.x+x, self.y+y, self.x+x+w, self.y+y+h, fill=c, width=borderw)

    def loadImgPIL(self, path):
        return Image.open("img/" + path)
    def loadImgTk(self, img):
        return ImageTk.PhotoImage(img)
    def loadImg(self, path):
        return self.loadImgTk(self.loadImgPIL(path))

    def drawImg(self, x, y, img, anchor="nw"):
        self.g.create_image(x, y, image=img, anchor=anchor)

    def fullClear(self):
        self.g.delete(ALL)
        self.clear(self.colors.bg)
    def clear(self, c):
        self.drawRect(c, 0, 0, self.width, self.height)


#     Things Chiel used in his win class and might be usefull later on
#     @staticmethod
#     def get_coords(lines, pos):
#         """Compute the coordinates of pos in lines."""
#         y = 0
#         line_beg = 0
#         for line in lines:
#             if pos <= line_beg + len(line):
#                 break
#             y += 1
#             line_beg += len(line)
# 
#         x = (pos - line_beg)
# 
#         return x, y
# 
#     def crop(self, string, center):
#         """Crop the string around center."""
#         assert 0 <= center < len(string)
#         lines = string.split('\n')
# 
#         # Compensate for splitting
#         center -= len(lines) - 1
# 
#         # Compute the coordinates of center
#         x, y = self.get_coords(lines, center)
# 
#         # Crop vertically
#         yoffset = max(0, y - int(self.height / 2))
#         lines = [line for i, line in enumerate(lines) if yoffset <= i < self.height]
# 
#         # Crop horizontally
#         xoffset = max(0, x - int(self.width / 2))
#         lines = [line[xoffset:xoffset + self.width - 1] for line in lines]
# 
#         return '\n'.join(lines)
