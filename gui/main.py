from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from MattyControls import *
from textwin import TextWin
from settings import Settings


class Application(Frame):
    def __init__(self, settings, master=None):
        """The constructor"""
        Frame.__init__(self, master)
        master.title("fate - test")

        self.canvas = Cnvs(master)
        self.canvas.bind("<Button-1>", self.leftClick)
        self.canvas.bind("<Button-3>", self.rightClick)
        self.canvas.width = settings.width
        self.canvas.height = settings.height
        self.canvas.locateInside(self, d=-2)

        textWindow = TextWin(settings, self.canvas)

    def leftClick(self, event):
        pass

    def rightClick(self, event):
        pass


def main():
    """The main entrypoint for this application"""
    settings = Settings()
    root = Tk()
    root.geometry("{}x{}".format(settings.width - 4, settings.height - 4))
    app = Application(settings, master=root)
    app.mainloop()

if __name__ == '__main__':
    main()
