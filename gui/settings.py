from . import colors
from os.path import expanduser
from contextlib import suppress
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
        self.loadSettings('gfate-settings-default.json')

    def calcFontSizes(self):
        fonts = [tkinter.font.Font(family=fam, size=pt) for fam, pt in [self.uifont, self.userfont]]
        self.uifontsize = Size(fonts[0].measure('a'), fonts[0].metrics('linespace'))
        self.userfontsize = Size(fonts[1].measure('a') , fonts[1].metrics('linespace'))

    def load(self):
        """Load all the settings from json file"""
        path = expanduser('~') + '/.fate/gfate-settings.json'
        self.loadSettings(path)
    
    def loadSettings(self, path):
        # IO magic here
        try:
            with open(path, 'r') as fd:
                content = fd.read()
        except (FileNotFoundError, PermissionError) as e:
            print('Could not open the gfate settings.json file.')
            return

        # JSON magic here
        settings = json.loads(content)

        with suppress(KeyError): # Python 3.4+ only, but <3
            self.size = Size(settings['windowsize'][0], settings['windowsize'][1])
            self.uifont = (settings['uifont']['family'], settings['uifont']['size'])
            self.userfont = (settings['userfont']['family'], settings['userfont']['size'])
            self.tabsize = Size(settings['tabsize'][0], settings['tabsize'][1])
            self.tabwidthextra = settings['tabwidthextra']
            self.statuswinenabled = settings['statuswinenabled']
            self.commandsize = Size(settings['commandwindowsize'][0], settings['commandwindowsize'][1])
            self.fps_inv = 1 / settings['fps']                           # seconds per frame
            self.flickercount = settings['flickertime'] // self.fps_inv  # frames per cursor flicker change


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

