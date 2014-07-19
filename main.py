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
        master.title("Test")

        textWindow = TextWin(settings)


def main():
    """The main entrypoint for this application"""
    settings = Settings()
    root = Tk()
    root.geometry("{}x{}".format(settings.width, settings.height))
    app = Application(settings, master=root)
    app.mainloop()

if __name__ == '__main__':
    main()
