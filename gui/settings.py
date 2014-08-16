from . import colors
import tkinter.font


class Settings():
    """The settings class"""

    def __init__(self):
        self.width, self.height = 800, 500
        self.uifont = ('Consoloas', 10)
        self.userfont = ('Consolas', 10)
        self.tabwidth = 110
        self.tabheight = 36
        self.tabwidthextra = 30
        self.colors = colors.Colors()
        self.commandwidth = 300
        self.commandheight = 38
        self.flickertime = 400
        self.refresh_rate = 30
        self.calcFontWidths()

    def calcFontWidths(self):
        fonts = [tkinter.font.Font(family=fam, size=pt) for fam, pt in [self.uifont, self.userfont]]
        self.uifontsize = (fonts[0].measure('a'), fonts[0].metrics("linespace"))
        self.userfontsize = (fonts[1].measure('a') , fonts[1].metrics("linespace"))

    def load(self):
        """Load all the settings from json file"""
        pass

    def save(self):
        """Write the settings to a json file"""
        pass
