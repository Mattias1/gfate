About gfate
============

gfate is a GUI for Chiel92's fate text editor, strongly influenced by both vim and sublime text.
For the backend source code check [fate][fate] and for a (sometimes more up to date) terminal interface,
see [tfate][fate-tui] (it might not work on windows though).

It is in development phase.


Installation
=============
### Windows
Step 1: Make sure you have all dependencies installed: `python3`, `tkinter` and `PIL`.
First install [python3][python3], version 3.4 or above. It should install tkinter by default as well.
Then install PIL by running the `pip install pillow` command.

Step 2: Clone gfate and it's submodules: `git clone --recursive https://github.com/Mattias1/gfate`.
(Update with `git pull && git submodule update --init --recursive`).

Step 3: Navigate to the folder where fate is installed and run with `python3 fate foo.py bar.py`.

### Ubuntu
The installation is similar to windows, the only difference being that tkinter isn't automatically
installed and you can install the PIL library in the same way as tkinter.

`sudo apt-get install python3-pil.imagetk python3-tk`


[python3]: https://www.python.org/downloads/
[fate]: http://github.com/Chiel92/fate
[fate-tui]: http://github.com/Chiel92/fate-tui

