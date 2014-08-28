from . import colors
from os.path import expanduser
import tkinter.font
import json


class Settings():
    """The settings class"""

    def __init__(self):
        self.loadDefaults()
        self.load()
        self.colors = colors.Colors()
        self.calcFontSizes()

    def loadDefaults(self):
        self.size = Size(800, 500)
        self.uifont = ('Lucida Console', 10)
        self.userfont = ('Lucida Console', 10)
        self.tabsize = Size(110, 36)
        self.tabwidthextra = 30
        self.statuswinenabled = True
        self.commandsize = Size(300, 58)
        self.fps_inv = 1/30                       # seconds per frame
        self.flickercount = 0.400 // self.fps_inv # frames per cursor flicker change

    def calcFontSizes(self):
        fonts = [tkinter.font.Font(family=fam, size=pt) for fam, pt in [self.uifont, self.userfont]]
        self.uifontsize = Size(fonts[0].measure('a'), fonts[0].metrics('linespace'))
        self.userfontsize = Size(fonts[1].measure('a') , fonts[1].metrics('linespace'))

    def load(self):
        """Load all the settings from json file"""
        # IO magic here
        try:
            pathToUser = expanduser('~') + '/.fate/'
            with open(pathToUser + 'gfate-settings.json', 'r') as fd:
                content = fd.read()
        except (FileNotFoundError, PermissionError) as e:
            print('Could not open the gfate settings.json file.')
            return

        # JSON magic here
        obj = json.loads(content)

        self.size = Size(obj['windowsize'][0], obj['windowsize'][1])
        self.uifont = (obj['uifont']['family'], obj['uifont']['size'])
        self.userfont = (obj['userfont']['family'], obj['userfont']['size'])
        self.tabsize = Size(obj['tabsize'][0], obj['tabsize'][1])
        self.tabwidthextra = obj['tabwidthextra']
        self.statuswinenabled = obj['statuswinenabled']
        self.commandsize = Size(obj['commandwindowsize'][0], obj['commandwindowsize'][1])
        self.fps_inv = 1 / obj['fps']                           # seconds per frame
        self.flickercount = obj['flickertime'] // self.fps_inv  # frames per cursor flicker change


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
        if other is None:
            return False
        return self.x == other[0] and self.y == other[1]
    def __neq__(self, other):
        return not self == other

    def __str__(self):
        return '({}, {})'.format(self.x, self.y)


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
        if other is None:
            return False
        return self.w == other[0] and self.h == other[1]
    def __neq__(self, other):
        return not a == other

    def __str__(self):
        return '{}x{}'.format(self.w, self.h)

