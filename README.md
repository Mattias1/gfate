About gfate
============

gfate is a GUI for Chiel92's fate text editor, strongly influenced by both vim and sublime text.
For the backend source code check [fate][fate] and for a (sometimes more up to date) terminal interface,
see [tfate][tfate] (it might not work on windows though).

It is in development phase.


Installation
=============
### Windows
Step 1: Make sure you have all dependencies installed: `python3`, `tkinter` and `PIL`.
First install [python3][python3], version 3.4 or above. It should install tkinter by default as well.
Then install PIL by running the `pip install pillow` command.

(optionally) Rename the `python` executable to `python3` and add it to the path variable.

Step 2: Clone gfate and it's submodules: `git clone --recursive https://github.com/Mattias1/gfate`.
(Update with `git pull && git submodule update --init --recursive`).

Step 3: In a terminal emulator with admin priveleges, navigate to the folder where gfate is
installed and run `python3 install_win.py <installation_path> [<python_path>]`,
where `<installation_path>` is a path of your choice, e.g. `C:\\bin`,
and `<python_path>` optionally allows you to specify the correct path to the python interpreter.
It defaults to just `python`.

The installer will put two files in the `<installation_path>`,
`gfate` and `gfate.bat` which are startup scripts for
a unix emulation shell and a windows prompt respectively.
For ease of access it is recommended that the installation path is added to your PATH
environment variable.

The installation script also adds a key to the registry which allows you to edit files with
gfate by adding an option to the right click context menu.

To uninstall gfate, run `uninstall_win.py`, again providing the same installation path.
This time, the path to the python interpreter must not be provided.

### Ubuntu
Tkinter isn't automatically installed, as well as PIL, so you have to

`sudo apt-get install python3-pil.imagetk python3-tk`

There is no installation script yet.
You can create your own startup scripts and put these into a place that is in your PATH.


[python3]: https://www.python.org/downloads/
[fate]: http://github.com/Chiel92/fate
[tfate]: http://github.com/Chiel92/tfate

