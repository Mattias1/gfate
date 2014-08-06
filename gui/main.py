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

        self.canvas = Cnvs(master, bd=-2)
        self.canvas.bind("<Button-1>", self.onLeftClick)
        self.canvas.bind("<Button-3>", self.onRightClick)
        self.master.bind("<Key>", self.onKeyPress)
        self.resize_bind_id = self.master.bind("<Configure>", self.onResizeOrMove)
        self.canvas.highlightthickness = 0
        self.canvas.width = settings.width
        self.canvas.height = settings.height
        self.canvas.locateInside(self, d=0)

        self.textWindow = TextWin(settings, self.canvas)

        self.settings = settings

    def onLeftClick(self, event):
        print('OnLeftClick: {}, {}'.format(event.x, event.y))

    def onRightClick(self, event):
        print('OnRightClick: {}, {}'.format(event.x, event.y))

    def onKeyPress(self, event):
        print('OnKeyPress: {}'.format(repr(event.char)))

    def onResizeOrMove(self, event):
        w, h = event.width, event.height
        if w != self.settings.width or h != self.settings.height:
            self.settings.width, self.settings.height = w, h
            self.canvas.width, self.canvas.height = w, h
            self.textWindow.resize()


def main():
    """The main entrypoint for this application"""
    settings = Settings()
    root = Tk()
    root.configure(bg=settings.colors.bg)
    root.geometry("{}x{}".format(settings.width, settings.height))
    app = Application(settings, master=root)
    app.mainloop()

if __name__ == '__main__':
    main()
