class Colors():
    """The colors class"""

    def __init__(self):
        self.bg = "#888"
        self.tabbg = "#444"
        self.text = "#fff"
        self.tabtext = "#fff"

    def load(self):
        """Load all the colors from json file"""
        pass

    def save(self):
        """Write the colors to a json file"""
        pass


if __name__ == '__main__':
    import main
    main.main()
