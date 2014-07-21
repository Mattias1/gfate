class Settings():
    """The settings class"""

    def __init__(self):
        self.width, self.height = 800, 500
        self.uifont = ('Arial', 12)
        self.userfont = ('Consolas', 12)

    def load(self):
        """Load all the settings from json file"""
        pass

    def save(self):
        """Write the settings to a json file"""
        pass


if __name__ == '__main__':
    import main
    main.main()
