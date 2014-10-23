from tkinter import *
from tkinter.ttk import *
from mattycontrols.MattyControls import *
from .settings import Settings, Pos, Size


class Options(Toplevel):
    def __init__(self, master, app, settings):
        """The options frame"""
        Toplevel.__init__(self, app)
        self.geometry('{}x{}+{}+{}'.format(400, 250, 100, 100))
        master.title("gfate - Options")

        # The tab widgets
        tabHolder = Notebook(self)
        tabHolder.pack(fill='both', expand='yes')
        fontFrame = FontOptions(tabHolder, self, app, settings)
        tabHolder.add(fontFrame, text='Font')
        colorFrame = ColorOptions(tabHolder, self, app, settings)
        tabHolder.add(colorFrame, text='Colours')


class FontOptions(Frame):
    def __init__(self, master, optionsApp, mainApp, settings):
        """A frame that allows you to choose a font"""
        frame_init(self, master, True)

        self.dbPreset = Db(self, ['Sid', 'Manny', 'Diego'], 0)
        self.dbPreset.locateInside(self, H_LEFT, V_TOP)
        self.dbPreset.addLabel('Character: ')

        self.cbNotes = Cb(self, text="Don't check this checkbox")
        self.cbNotes.locateFrom(self.dbPreset, H_COPY_LEFT, V_BOTTOM)

        self.btnQuit = Btn(self, text='Quit', command=self.quit)
        self.btnQuit.locateInside(self, H_RIGHT, V_BOTTOM)


class ColorOptions(Frame):
    def __init__(self, master, optionsApp, mainApp, settings):
        """An options frame that allows you to choose a colour scheme"""
        frame_init(self, master, True)

        self.btnQuit = Btn(self, text='Quit', command=self.quit)
        self.btnQuit.locateInside(self, H_RIGHT, V_BOTTOM)

