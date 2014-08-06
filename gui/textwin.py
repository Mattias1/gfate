from win import *
from colors import *


class TextWin(Win):
    """The text window class
    
    This is the main window for the gfate text editor.
    """

    def __init__(self, settings, canvas):
        Win.__init__(self, settings, canvas)

        self.draw()

    def draw(self):
        self.fullClear()
        self.drawTabs()
        self.drawString("The layout of the fate GUI.", self.colors.text, 6, 40)


if __name__ == '__main__':
    import main
    main.main()
