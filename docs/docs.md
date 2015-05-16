A gui for fate
===============

Some things you need to know to make a gui for fate.

Variables
----------

- document.text:
    The string with all the characters in the file
    Alternative: document.view.text: this contains replacements for the gui to show
    For example: '\t' -> '·   ', '\n' -> ' \n', ' ' -> '·'

- document.highlighting:
    A list of labels per character.
    Values: string, number, keyword, comment
    Alternative: document.view.highlighting

- document.selection:
    A list of intervals with all the selections (== cursor positions). In the most normal case that
    is a single interval with lenght 1; like the vim cursor.
    Alternative: document.view.selection

API
----

The fate API is the main point of communication between the backend and the gui. It contains methods
that the UI should implement. The most important one being ```_getuserinput```, that when called
asks for the last keypress of the user (which should be stored in the ```api.inputqueue```) and
```touch```, that is called everytime something is changed (like a character added to
```document.text```).

