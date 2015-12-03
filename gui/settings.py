from . import colors
from os.path import expanduser
from contextlib import suppress
import tkinter.font
import json


class Settings():
    """The settings class"""

    def __init__(self, rootpath):
        self.colors = colors.Colors(rootpath)
        self.loadDefaults(rootpath)
        self.load()

    def loadDefaults(self, rootpath):
        result = self.loadSettings(rootpath + 'settings-default.json')
        assert result, 'Could not load default settings!'

    def calcSettings(self):
        # The font sizes
        fonts = [tkinter.font.Font(family=fam, size=pt) for fam, pt in [self.uifont, self.userfont]]
        self.uifontsize = Size(fonts[0].measure('a'), fonts[0].metrics('linespace'))
        self.userfontsize = Size(fonts[1].measure('a') , fonts[1].metrics('linespace'))
        # The scroll bar width (will be set at scrollbar img initialization)
        self.scrollbarwidth = 0
        # The Status window size
        self.statusheight = self.uifontsize.h + 6
        # Line number margin
        self.linenumbermargin = 2

    def load(self):
        """Load all the settings from json file"""
        path = expanduser('~') + '/.fate/gfate/settings.json'
        self.loadSettings(path)

    def loadSettings(self, path):
        # IO magic here
        try:
            with open(path, 'r') as fd:
                content = fd.read()
        except (FileNotFoundError, PermissionError) as e:
            print('Could not open the gfate settings.json file.')
            return False

        # JSON magic here
        try:
            settings = json.loads(content)
        except:
            print('Error parsing the json file (' + path + ')')
            return False

        with suppress(KeyError):
            self.pos = Pos(settings['windowpos'][0], settings['windowpos'][1])
        with suppress(KeyError):
            self.size = Size(settings['windowsize'][0], settings['windowsize'][1])
        with suppress(KeyError):
            self.commandsize = Size(settings['commandwindowsize'][0], settings['commandwindowsize'][1])
        with suppress(KeyError):
            self.uifont = (settings['uifont']['family'], settings['uifont']['size'])
        with suppress(KeyError):
            self.userfont = (settings['userfont']['family'], settings['userfont']['size'])
        with suppress(KeyError):
            self.tabsize = Size(settings['tabsize'][0], settings['tabsize'][1])
        with suppress(KeyError):
            self.tabwidthextra = settings['tabwidthextra']
        with suppress(KeyError):
            self.tabname = settings['tabname']
        with suppress(KeyError):
            self.statuswinenabled = settings['statuswinenabled']
        with suppress(KeyError):
            self.maxerrorlines = settings['maxerrorlines']
        with suppress(KeyError):
            self.scrolllines = settings['scrolllines']
        with suppress(KeyError):
            self.scrollbars = settings['scrollbars']
        with suppress(KeyError):
            self.minimumscrollbarsize = settings['minimumscrollbarsize']
        with suppress(KeyError):
            self.linenumbers = settings['linenumbers']
        with suppress(KeyError):
            self.fps_inv = 1 / settings['fps']                                  # seconds per frame
        with suppress(KeyError):
            self.flickercount = int(settings['flickertime'] // self.fps_inv)    # frames per cursor flicker change
        colorsfile = ''
        with suppress(KeyError):
            colorsfile = settings['colors']
        if colorsfile != '':
            self.colors.load(colorsfile)

        # Calculate some settings based on loaded settings
        self.calcSettings()
        return True


class Pos():
    """A position class just to make things a bit easier."""
    def __init__(self, x, y=None):
        if y == None:
            self.x, self.y = x[0], x[1]
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

    def __mul__(self, constant):
        return Size(constant * self.x, constant * self.y)
    def __rmul__(self, constant):
        return self * constant

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
            self.w, self.h = w[0], w[1]
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

    def __mul__(self, constant):
        return Size(constant * self.w, constant * self.h)
    def __rmul__(self, constant):
        return self * constant

    def __eq__(self, other):
        if other is None:
            return False
        return self.w == other[0] and self.h == other[1]
    def __neq__(self, other):
        return not a == other

    def __str__(self):
        return '{}x{}'.format(self.w, self.h)

