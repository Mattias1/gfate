from os.path import expanduser
import json


class Colors():
    """The colors class"""

    def __init__(self, rootpath):
        self.rootpath = rootpath

    #
    # Json loading functions
    #
    def load(self, colorsfile):
        """Load all the colors from json file"""
        try:
            path = self.rootpath + 'colors/' + colorsfile + '.json'
            self.loadColors(path)
        except (FileNotFoundError, PermissionError) as e:
            try:
                path = expanduser('~') + '/.fate/gfate/' + colorsfile + '.json'
                self.loadColors(path)
            except:
                print('Could not open the gfate settings.json file.')
                return
        self.loadColors(path)

    def loadColors(self, path):
        # IO magic here
        with open(path, 'r') as fd:
            content = fd.read()

        # JSON magic here
        settings = json.loads(content)

        self.bg = settings['bg']
        self.linenumber = settings['linenumber']
        self.selectionbg = settings['selectionbg']

        self.text = settings['text']
        self.string = settings['string']
        self.number = settings['number']
        self.keyword = settings['keyword']
        self.comment = settings['comment']

        self.activetab = settings['activetab']
        self.activetabbg = settings['activetabbg']
        self.inactivetab = settings['inactivetab']
        self.inactivetabbg = settings['inactivetabbg']
        self.headerbg = settings['headerbg']

        self.scroll = settings['scroll']
        self.scrollbg = settings['scrollbg']
        self.gear = settings['gear']

    #
    # Helper functions
    #
    def toTuple(self, color):
        """Convert a hexadecimal colour to a integer tuple"""
        c = int(color[1:], 16)
        return ((c >> 16) & 255, (c >> 8) & 255, c & 255)
    def toHex(self, color):
        """Convert a hexadecimal colour to a integer tuple"""
        return '#{}{}{}'.format(hex(color[0])[2:], hex(color[1])[2:], hex(color[2])[2:])

    def hexlerp(self, a, b, v):
        """Linearely interpolate between two colours a and b"""
        c, d = self.toTuple(a), self.toTuple(b)
        return self.toHex([int(c[i] + (d[i] - c[i]) * v) for i in range(3)])

    def fromLabel(self, label):
        if label == 'string':
            return self.string
        if label == 'number':
            return self.number
        if label == 'keyword':
            return self.keyword
        if label == 'comment':
            return self.comment
        return self.text

