from win import *
from colors import *


class TextWin(Win):
    """The settings class"""

    def __init__(self, settings, canvas):
        Win.__init__(self, settings, canvas)

        self.img = self.loadImg("space.png")
        self.draw()

    def draw(self):
        self.fullClear("black")
        self.drawRect("red", 0, 0, 151, 200)
        self.drawString("Hi there", "white", 60, 0)
        self.drawImg(100, 100, self.img)


if __name__ == '__main__':
    import main
    main.main()
