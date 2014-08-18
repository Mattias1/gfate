from . import colors
# import tkinter.font
from PIL import ImageFont


class Settings():
    """The settings class"""

    def __init__(self):
        self.size = Size(800, 500)
        # self.uifont = ('Consolas', 10)
        # self.userfont = ('Consolas', 10)
        self.uifont = ImageFont.truetype('Consola.ttf', 13)
        self.userfont = ImageFont.truetype('Consola.ttf', 13)
        self.tabsize = Size(110, 36)
        self.tabwidthextra = 30
        self.colors = colors.Colors()
        self.commandsize = Size(300, 38)
        self.flickertime = 400
        self.refresh_rate = 30
        self.calcFontWidths()

    def calcFontWidths(self):
        self.uifontsize = Size(self.uifont.getsize('a'))
        self.userfontsize = Size(self.userfont.getsize('a'))
        # fonts = [tkinter.font.Font(family=fam, size=pt) for fam, pt in [self.uifont, self.userfont]]
        # self.uifontsize = Size(fonts[0].measure('a'), fonts[0].metrics("linespace"))
        # self.userfontsize = Size(fonts[1].measure('a') , fonts[1].metrics("linespace"))

    def load(self):
        """Load all the settings from json file"""
        pass

    def save(self):
        """Write the settings to a json file"""
        pass


class Pos():
    """A position class just to make things a bit easier."""
    def __init__(self, x, y=None):
        if y == None:
            self.x, self.y = x
        else:
            self.x, self.y = x, y

    @property
    def t(self):
        return (self.x, self.y)

    def __getitem__(self, i):
        if i==0:
            return self.x
        return self.y

    def __add__(self, other):
        return Pos(self.x + other[0], self.y + other[1])
    def __radd__(self, other):
        return other + self
    def __sub__(self, other):
        return self + (-other[0], -other[1])

    def __eq__(self, other):
        return self.x == other[0] and self.y == other[1]
    def __neq__(self, other):
        return not self == other


class Size():
    """A size class just to make things a bit easier."""
    def __init__(self, w, h=None):
        if h == None:
            self.w, self.h = w
        else:
            self.w, self.h = w, h

    @property
    def t(self):
        return (self.w, self.h)

    def __getitem__(self, i):
        if i==0:
            return self.w
        return self.h

    def __add__(self, other):
        return Size(self.w + other[0], self.h + other[1])
    def __radd__(self, other):
        return other + self
    def __sub__(self, other):
        return self + (-other[0], -other[1])

    def __eq__(self, other):
        return self.w == other[0] and self.h == other[1]
    def __neq__(self, other):
        return not a == other

