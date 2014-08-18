"""
Module containing Win class.
The Win class is meant to hide some common interaction with curses.
"""
from tkinter import *
from PIL import Image, ImageTk, ImageDraw
from .settings import *
from .colors import *


class Win:
    """Abstract window class"""

    def __init__(self, settings, app, s=None, p=Pos(0,0)):
        self.settings = settings
        self.colors = settings.colors
        self.enabled = True
        self.app = app
        self.canvas = app.canvas
        self.pos = p
        self.size = None
        self.resize(s, False)

    @property
    def g(self):
        return self.app.mainWindow.gfx

    def enable(self):
        """Enable this window."""
        self.enabled = True

    def disable(self):
        """Disable this window."""
        self.enabled = False

    def quit(self):
        """Quit the application"""
        self.app.quit()

    def inside(self, p):
        return self.pos.x <= p.x <= self.pos.x + self.size.w and self.pos.y <= p.y <= self.pos.y + self.size.h

    def onMouseDown(self, p, btnNr):
        pass
    def onMouseMove(self, p, btnNr):
        pass
    def onMouseUp(self, p, btnNr):
        pass
    def onKeyDown(self, c):
        pass

    def resize(self, s=None, draw=True):
        """Resize window."""
        if s == None:
            s = self.settings.size
        self.size = s
        if draw:
            self.draw()

    def loop(self):
        """This method is being called every X miliseconds"""
        return False

    def draw(self):
        """This draw method needs to be overridden to draw the window content."""
        pass

    # Some draw methods to make sure all my subclasses don't have to bother about tkinters canvas
    def drawFString(self, text, c, p, font, anchor="nw"):
        self.g.text((self.pos + p).t, text, font=font)
        # self.g.create_text((self.pos + p).t, anchor=anchor, text=text, fill=c, font=font)
    def drawUIString(self, text, c, p, anchor="nw"):
        self.drawFString(text, c, p, self.settings.uifont, anchor=anchor)
    def drawString(self, text, c, p, anchor="nw"):
        self.drawFString(text, c, p, self.settings.userfont, anchor=anchor)

    def drawLine(self, c, p, q, w=1):
        self.g.line([(self.pos + p).t, (self.pos + q).t], fill=c, width=w)
        # self.g.create_line((self.pos + p).t, (self.pos + q).t, fill=c)

    def drawRect(self, c, p, s):
        self.drawRectBorder(c, p, s, 0)
    def drawRectBorder(self, c, p, s, borderw=1):
        self.g.rectangle([(self.pos + p).t, (self.pos + p + s - (1, 1)).t], fill=c)
        # self.g.create_rectangle((self.pos + p).t, (self.pos + p + s).t, fill=c, width=borderw)
        # TODO: use the border width

    def loadImgPIL(self, path):
        return Image.open("img/" + path)
    def loadImgTk(self, img):
        return ImageTk.PhotoImage(img)
    def loadImg(self, path):
        return self.loadImgTk(self.loadImgPIL(path))

    def drawImg(self, p, img, anchor="nw"):
        r, g, b, a = img.split()
        top = Image.merge('RGB', (r, g, b))
        mask = Image.merge('L', (a, ))
        self.app.mainWindow.im.paste(top, (self.pos + p).t, mask)
        # self.g.create_image((self.pos + p).t, image=img, anchor=anchor)

    def clear(self, c):
        self.drawRect(c, Pos(0, 0), self.size)

    def drawcursor(self, p, cursorvisible):
        if cursorvisible:
            _, h = self.settings.userfontsize.t
            self.drawLine(self.colors.text, p, p + (0, h))


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
