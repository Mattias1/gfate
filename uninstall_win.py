#!python3
"""Script which uninstalls gfate on windows."""

import os
import sys

path_to_main = os.path.dirname(os.path.abspath(__file__)) + '\\main.py'

try:
    installation_dir = sys.argv[1]
except IndexError:
    exit('Need to provide installation directory')

# Remove bat file in installation directory
try:
    os.remove(installation_dir + '\\gfate.bat')
except FileNotFoundError:
    print('gfate.bat seems to be removed already')

# Remove shell file in installation directory
try:
    os.remove(installation_dir + '\\gfate')
except FileNotFoundError:
    print('gfate shell script seems to be removed already')

# Remove registry key to open files in gfate from context menu
import winreg as wreg
reg = wreg.ConnectRegistry(None, wreg.HKEY_CLASSES_ROOT)
root = wreg.OpenKey(reg, r'\*\shell')
key = wreg.OpenKey(root, r'Open with gfate')
wreg.DeleteKey(key, 'command')
wreg.DeleteKey(root, 'Open with gfate')
