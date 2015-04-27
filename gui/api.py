import fate.userinterface

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
        self.redraw()

    def notify(self, message):
        # This method is called from a different thread (the one fate runs in)
        raise NotImplementedError()

    def _getuserinput(self):
        # This method is called from a different thread (the one fate runs in)
        # Block untill you have something
        while not self.inputqueue:
            sleep(self.settings.fps_inv)
        return self.inputqueue.popleft()
    @property
    def viewport_size(self):
        return self.textRange.t

    @property
    def viewport_offset(self):
        return self._displayIndex

    @viewport_offset.setter
    def viewport_offset(self, value):
        self._displayIndex = value
        self._displayOffset = self.getCoordFromChar(value)
        self.redraw()

    #
    # Implement UI commands
    #
    def command_mode(self, command_string=':'):
        # This method is called from a different thread (the one fate runs in)
        raise NotImplementedError()

