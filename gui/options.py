from tkinter import *
from tkinter.ttk import *
from mattycontrols.MattyControls import *
from .settings import Settings, Pos, Size


class Options(Toplevel):
    def __init__(self, app, settings, master):
        """The options frame"""
        frame_init(self, master)
        master.title("gfate - Options")

        self.app = app
        self.settings = settings

        self.dbPreset = Db(self, ['guitar', 'soprano ukelele', 'tenor ukelele'], 0)
        self.dbPreset.locateInside(self, H_LEFT, V_TOP)
        self.dbPreset.addLabel('Preset: ')
        self.dbPreset.onChange = lambda *args: self.onChangeAnything()

        self.cbNotes = Cb(self, text='Display notes')
        self.cbNotes.locateFrom(self.dbPreset, H_COPY_LEFT, V_BOTTOM)
        self.cbNotes.onChange = lambda *args: self.onChangeAnything()

        self.btnQuit = Btn(self, text='Quit', command=self.quit)
        self.btnQuit.locateInside(self, H_RIGHT, V_BOTTOM)

