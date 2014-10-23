from tkinter import *
from tkinter.ttk import *
from mattycontrols.MattyControls import *
from .settings import Settings, Pos, Size


#
# Helper classes
#
# The Toplevel class (this is the window that manages the tabs)
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


# An optionsframe with some predefined methods
class OptionsFrame(Frame):
    def init(self, master, optionsApp, mainApp, settings):
        frame_init(self, master, True)

        self.master = master
        self.optionsApp = optionsApp
        self.mainApp = mainApp
        self.settings = settings
        self.colors = settings.colors


#
# The actual frames
#
class FontOptions(OptionsFrame):
    def __init__(self, master, optionsApp, mainApp, settings):
        """A frame that allows you to choose a font"""
        self.init(master, optionsApp, mainApp, settings)

        self.dbPreset = Db(self, ['Sid', 'Manny', 'Diego'], 0)
        self.dbPreset.locateInside(self, H_LEFT, V_TOP)
        self.dbPreset.addLabel('Character: ')

        self.cbNotes = Cb(self, text="Don't check this checkbox")
        self.cbNotes.locateFrom(self.dbPreset, H_COPY_LEFT, V_BOTTOM)

        self.btnQuit = Btn(self, text='Quit', command=self.optionsApp.destroy)
        self.btnQuit.locateInside(self, H_RIGHT, V_BOTTOM)


class ColorOptions(OptionsFrame):
    def __init__(self, master, optionsApp, mainApp, settings):
        """An options frame that allows you to choose a colour scheme"""
        self.init(master, optionsApp, mainApp, settings)

        self.btnQuit = Btn(self, text='Quit', command=self.optionsApp.destroy)
        self.btnQuit.locateInside(self, H_RIGHT, V_BOTTOM)

