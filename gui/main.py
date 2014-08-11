from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from MattyControls import *
from mainwin import MainWin
from settings import Settings


class Application(Frame):
    def __init__(self, settings, master=None):
        """The constructor"""
        Frame.__init__(self, master)
        master.title("fate - test")

        self.canvas = Cnvs(master, bd=-2)
        self.canvas.bind("<Button-1>", self.onLeftDown)
        self.canvas.bind("<Button-2>", self.onScrollDown)
        self.canvas.bind("<Button-3>", self.onRightDown)
        self.canvas.bind("<B1-Motion>", self.onLeftMove)
        self.canvas.bind("<B2-Motion>", self.onScrollMove)
        self.canvas.bind("<B3-Motion>", self.onRightMove)
        self.canvas.bind("<ButtonRelease-1>", self.onLeftUp)
        self.canvas.bind("<ButtonRelease-2>", self.onScrollUp)
        self.canvas.bind("<ButtonRelease-3>", self.onRightUp)
        self.master.bind("<Key>", self.onKeyDown)
        self.resize_bind_id = self.master.bind("<Configure>", self.onResizeOrMove)
        self.canvas.highlightthickness = 0
        self.canvas.width = settings.width
        self.canvas.height = settings.height
        self.canvas.locateInside(self, d=0)

        self.mainWindow = MainWin(settings, self)

        self.settings = settings

    def onLeftDown(self, event):
        self.mainWindow.onMouseDown(event.x, event.y, 1)
        print('OnLeftDown: {}, {}'.format(event.x, event.y))
    def onScrollDown(self, event):
        self.mainWindow.onMouseDown(event.x, event.y, 2)
        print('OnScrollDown: {}, {}'.format(event.x, event.y))
    def onRightDown(self, event):
        self.mainWindow.onMouseDown(event.x, event.y, 3)
        print('OnRightDown: {}, {}'.format(event.x, event.y))

    def onLeftMove(self, event):
        self.mainWindow.onMouseMove(event.x, event.y, 1)
        print('OnLeftMove: {}, {}'.format(event.x, event.y))
    def onScrollMove(self, event):
        self.mainWindow.onMouseMove(event.x, event.y, 2)
        print('OnScrollMove: {}, {}'.format(event.x, event.y))
    def onRightMove(self, event):
        self.mainWindow.onMouseMove(event.x, event.y, 3)
        print('OnRightMove: {}, {}'.format(event.x, event.y))

    def onLeftUp(self, event):
        self.mainWindow.onMouseUp(event.x, event.y, 1)
        print('OnLeftUp: {}, {}'.format(event.x, event.y))
    def onScrollUp(self, event):
        self.mainWindow.onMouseUp(event.x, event.y, 2)
        print('OnScrollUp: {}, {}'.format(event.x, event.y))
    def onRightUp(self, event):
        self.mainWindow.onMouseUp(event.x, event.y, 3)
        print('OnRightUp: {}, {}'.format(event.x, event.y))

    def onKeyDown(self, event):
        print('OnKeyPress: {}'.format(repr(event.char)))

    def onResizeOrMove(self, event):
        w, h = event.width, event.height
        if w != self.settings.width or h != self.settings.height:
            self.settings.width, self.settings.height = w, h
            self.canvas.width, self.canvas.height = w, h
            self.mainWindow.resize()


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
