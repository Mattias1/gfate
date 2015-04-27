import fate.userinterface
from time import sleep

class API(fate.userinterface.UserInterfaceAPI):
    """
    The class that communicates with fate
    """
    def __init__(self, doc, win):
        fate.userinterface.UserInterfaceAPI.__init__(self, doc)
        self.win = win

    #
    # Implement UserInterface methods
    #
    def touch(self):
        # This method is called from a different thread (the one fate runs in)
        self.win.redraw()

    def notify(self, message):
        # This method is called from a different thread (the one fate runs in)
        raise NotImplementedError()

    def _getuserinput(self):
        # This method is called from a different thread (the one fate runs in)
        # Block untill you have something
        while not self.inputqueue:
            sleep(self.win.settings.fps_inv)
        return self.inputqueue.popleft()
    @property
    def viewport_size(self):
        return self.win.textRange.t

    @property
    def viewport_offset(self):
        return self.win._displayIndex

    @viewport_offset.setter
    def viewport_offset(self, value):
        self.win._displayIndex = value
        self.win._displayOffset = self.win.getCoordFromChar(value)
        self.win.redraw()

    #
    # Implement UI commands
    #
    def command_mode(self, command_string=':'):
        # This method is called from a different thread (the one fate runs in)
        raise NotImplementedError()

