class Colors():
    """The colors class"""

    def __init__(self):
        self.bg = "#272822"
        self.text = "#eeeeee"
        self.selectionbg = "#575852"
        self.inactivetab = "#474842"
        self.tabbg = "#171714"
        self.tabtext = "#eeeeee"

    def load(self):
        """Load all the colors from json file"""
        pass

    def save(self):
        """Write the colors to a json file"""
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

if __name__ == '__main__':
    import main
    main.main()
