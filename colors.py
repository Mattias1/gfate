class Colors():
    """The colors class"""

    def __init__(self):
        self.bg = "#272822"
        self.text = "#eeeeee"
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

if __name__ == '__main__':
    import main
    main.main()
