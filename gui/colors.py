class Colors():
    """The colors class"""

    def __init__(self):
        self.loadDefaults()

    def loadDefaults(self):
        self.bg = '#272822'
        self.text = '#eeeeee'
        self.linenumber = '#777777'
        self.selectionbg = '#575852'
        self.inactivetab = '#474842'
        self.tabbg = '#171714'
        self.tabtext = '#eeeeee'
        self.scroll = '#737373'
        self.scrollbg = '#1d1d1d'

    def load(self):
        """Load all the colors from json file"""
        pass

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
            return '#e6db74'
        if label == 'number':
            return '#ae81ff'
        if label == 'keyword':
            return '#f92672'
        if label == 'comment':
            return '#75715e'
        return self.text

