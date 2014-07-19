"""
Module containing Win class.
The Win class is meant to hide some common interaction with curses.
"""
from settings import *


class Win:
    """Abstract window class"""

    def __init__(self, settings, width=None, height=None, x=0, y=0):
        self.settings = settings
        self.resize(width, height)
        self.x, self.y = x, y
        self.enabled = True

    def enable(self):
        """Enable this window."""
        self.enabled = True

    def disable(self):
        """Disable this window."""
        self.enabled = False

    def resize(self, w=None, h=None):
        """Resize window."""
        if w == None:
            w = self.settings.width
        if h == None:
            h = self.settings.height
        self.width, self.height = w, h
        self.draw()

    def draw(self):
        """This draw method needs to be overridden to draw the window content."""
        pass

#     @staticmethod
#     def get_coords(lines, pos):
#         """Compute the coordinates of pos in lines."""
#         y = 0
#         line_beg = 0
#         for line in lines:
#             if pos <= line_beg + len(line):
#                 break
#             y += 1
#             line_beg += len(line)
# 
#         x = (pos - line_beg)
# 
#         return x, y
# 
#     def crop(self, string, center):
#         """Crop the string around center."""
#         assert 0 <= center < len(string)
#         lines = string.split('\n')
# 
#         # Compensate for splitting
#         center -= len(lines) - 1
# 
#         # Compute the coordinates of center
#         x, y = self.get_coords(lines, center)
# 
#         # Crop vertically
#         yoffset = max(0, y - int(self.height / 2))
#         lines = [line for i, line in enumerate(lines) if yoffset <= i < self.height]
# 
#         # Crop horizontally
#         xoffset = max(0, x - int(self.width / 2))
#         lines = [line[xoffset:xoffset + self.width - 1] for line in lines]
# 
#         return '\n'.join(lines)
