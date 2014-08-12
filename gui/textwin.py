from win import *
from colors import *


class TextWin(Win):
    """The text window class
    
    This class represents the window for a single file.
    """

    def __init__(self, settings, app, title):
        Win.__init__(self, settings, app)

        self.title = title

    def draw(self):
        self.drawString("The layout of the fate GUI.\nThe title of this textwin is '{}'.".format(self.title), self.colors.text, 6, 40)


if __name__ == '__main__':
    import main
    main.main()
