from win import *


class TextWin(Win):
    """The settings class"""

    def __init__(self, settings, canvas):
        Win.__init__(self, settings, canvas)

    def draw(self):
        self.clear("black")


if __name__ == '__main__':
    import main
    main.main()
