from colors import *


class Settings():
    """The settings class"""

    def __init__(self):
        self.width, self.height = 800, 500
        self.uifont = ('Consoloas', 10)
        self.userfont = ('Consolas', 10)
        self.tabwidth = 110
        self.tabwidthextra = 30
        self.colors = Colors()

    def load(self):
        """Load all the settings from json file"""
        pass

    def save(self):
        """Write the settings to a json file"""
        pass


if __name__ == '__main__':
    import main
    main.main()
