from win import Win


class TextWin(Win):
    """The settings class"""

    def __init__(self, settings):
        Win.__init__(self, settings)

    def load(self):
        """Load all the settings from json file"""
        pass

    def save(self):
        """Save the settings to a json file"""
        pass


if __name__ == '__main__':
    import main
    main.main()
