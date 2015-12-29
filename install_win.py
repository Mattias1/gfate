#!python3
"""Script which installs gfate on windows."""

import os
import sys

path_to_main = os.path.dirname(os.path.abspath(__file__)) + '\\main.py'

try:
    installation_dir = sys.argv[1]
except IndexError:
    exit('Need to provide installation directory')

try:
    path_to_python = sys.argv[2]
except IndexError:
    path_to_python = 'python'


# Create bat file in installation directory
path_to_bat = installation_dir + '\\gfate.bat'
with open(path_to_bat, 'w') as f:
    f.write('"{}" "{}" "%*"'.format(path_to_python, path_to_main))

# Create shell file in installation directory
with open(installation_dir + '\\gfate', 'w') as f:
    f.write('"{}" "{}" "$@"'.format(path_to_python, path_to_main))


# Create registry key to open files in gfate from context menu
import winreg as wreg
reg = wreg.ConnectRegistry(None, wreg.HKEY_CLASSES_ROOT)
root = wreg.OpenKey(reg, r'\*\shell')
key = wreg.CreateKey(root, r'Open with gfate\command')
wreg.SetValue(key, None, wreg.REG_SZ, '{} %1'.format(path_to_bat))


# SHORTCUT, not working yet

# Create shortcut on Desktop
# import os
# from win32com.client import Dispatch

# import winshell
# desktop = winshell.desktop()

# desktop = os.path.join(os.getenv('userprofile'), 'desktop')

# path = os.path.join(desktop, "some_file.mp3.lnk")
# target = r"D:\Users\Myself\My Music\some_file.mp3"
# wDir = r"D:\Users\Myself\My Music"
# icon = r"D:\Users\Myself\My Music\some_file.mp3"

# shell = Dispatch('WScript.Shell')
# shortcut = shell.CreateShortCut(path)
# shortcut.Targetpath = target
# shortcut.WorkingDirectory = wDir
# shortcut.IconLocation = icon
# shortcut.save()


