"""
Module containing Win class.
The Win class is meant to hide some common interaction with curses.
"""
from tkinter import *
from PIL import Image, ImageTk
from settings import *
from colors import *
import copy


class Win:
    """Abstract window class"""

    def __init__(self, settings, canvas, width=None, height=None, x=0, y=0):
        self.settings = settings
        self.colors = settings.colors
        self.enabled = True
        self.g = canvas
        self.x, self.y = x, y
        self.resize(width, height)
        self.initTabs()

    def enable(self):
        """Enable this window."""
        self.enabled = True

    def disable(self):
        """Disable this window."""
        self.enabled = False

    def resize(self, w=None, h=None):
        """Resize window."""
        if w == None:
            w = self.settings.width
        if h == None:
            h = self.settings.height
        self.width, self.height = w, h

    def draw(self):
        """This draw method needs to be overridden to draw the window content."""
        pass

    # Some draw methods to make sure all my subclasses don't have to bother about tkinters canvas
    def drawFString(self, text, c, x, y, font, anchor="nw"):
        self.g.create_text(x, y, anchor=anchor, text=text, fill=c, font=font)
    def drawUIString(self, text, c, x, y, anchor="nw"):
        self.drawFString(text, c, x, y, self.settings.uifont, anchor=anchor)
    def drawString(self, text, c, x, y, anchor="nw"):
        self.drawFString(text, c, x, y, self.settings.userfont, anchor=anchor)

    def drawLine(self, c, x, y, p, q, w=1):
        self.g.create_line(x, y, p, q, fill=c) # Todo: use the line width

    def drawRect(self, c, x, y, w, h):
        self.g.create_rectangle(x, y, x+w, y+h, fill=c, width=0)
    def drawRectBorder(self, c, x, y, w, h, borderw=1):
        self.g.create_rectangle(x, y, x+w, y+h, fill=c, width=borderw)

    def loadImgPIL(self, path):
        return Image.open("../img/" + path)
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
        self.drawRect(c, self.x, self.y, self.width, self.height)

    # Tabs
    def initTabs(self):
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
        piltabs[6] = piltabs[6].resize((self.settings.width, h), Image.NEAREST)

        # Convert the images to Tk images
        self.tabImg = [self.loadImgTk(t) for t in piltabs]

    def drawTab(self, x, y, text, active=False):
        offset = 0 if active else 3
        w, h = self.tabImg[offset].width(), self.tabImg[offset].height()
        self.drawImg(x, y, self.tabImg[offset])
        self.drawImg(x + w, y, self.tabImg[1 + offset])
        self.drawImg(x + w + self.settings.tabwidth, y, self.tabImg[2 + offset])
        self.drawUIString(text, self.colors.tabtext, x + w + self.settings.tabwidth // 2, y + h // 2 + 2, "center")

    def drawTabs(self, y=3):
        # Draw tab background
        w = self.settings.tabwidth + 30
        self.drawRect(self.colors.tabbg, 0, 0, self.settings.width, y + self.tabImg[0].height())
        # Draw inactive tabs
        self.drawTab(0, y, 'inactive tab')
        self.drawTab(w, y, 'inactive tab')
        self.drawTab(3 * w, y, 'inactive tab')
        # Draw tab bottom
        self.drawImg(0, y, self.tabImg[6])
        # Draw the active tab
        self.drawTab(2 * w, y, 'active tab', True)


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


if __name__ == '__main__':
    import main
    main.main()
