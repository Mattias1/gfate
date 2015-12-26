#!python3
"""Top level script which runs fate."""

import os
import sys

libs_path = os.path.dirname(os.path.abspath(__file__)) + '/libs/'
libs_path_fate = os.path.dirname(os.path.abspath(__file__)) + '/libs/fate/'
sys.path.insert(0, libs_path)
sys.path.insert(0, libs_path_fate)

# Make sure fate can be imported anywhere (also from the user script).
# This way we can:
# - run fate without having it installed
# - and thus easily test development source
# - have multiple fate packages, in case we would use multiple user interfaces.

import tkinter
import gui.app
import gui.settings
import fate
import threading
import logging
import contextlib

# Create gfate
root = tkinter.Tk()
rootpath = os.path.dirname(os.path.abspath(__file__)) + '/'
settings = gui.settings.Settings(rootpath)
root.configure(bg="#000000")
root.geometry('{}x{}+{}+{}'.format(settings.size.w, settings.size.h, settings.pos.x, settings.pos.y))
app = gui.app.Application(settings, root, rootpath)

# Create fate
filenames = sys.argv[1:] or ['']
fate.document.Document.create_userinterface = app.mainWindow.addWin
for filename in filenames:
    doc = fate.document.Document(filename)
fate.document.documentlist[0].activate()

# Start fate
thread = threading.Thread(target=fate.run)
app.fateThread = thread
thread.start()

# Forward the fate logging to the standard out (debug)
# logging.getLogger().addHandler(logging.StreamHandler())

try:
    # Start gfate
    app.mainloop()

    # If fate crashes, close the gfate gui and leave a message (aka, keep the console alive)
    with contextlib.suppress(AttributeError):
        if app.quitOnFateError:
            root.destroy()
            print('====================\n  UNEXPECTED ERROR\n====================')
            print('gfate detected that the fate core thread is no longer active.\nPress enter to quit...')
            input()
except:
    # If gfate crashes, close the fate core
    fate.commands.force_quit()
    raise
