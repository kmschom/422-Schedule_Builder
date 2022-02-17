class ManagerInterface:
    def __init__(self, scheduleExists, signalSchedule):
        self.scheduleExists = scheduleExists
        self.signalSchedule = signalSchedule
        self._createDisplay()

    def _createDisplay(self):
        #Initialize tkinter window and set its properties
        self._updateDisplay()

    def _updateDisplay(self):
        #Will be called by inside code to delete everything and re-add them to
        #tkinter window

    def _startScheduling(self, filePaths):
        #Will be called when the file input is done
        signalSchedule(filePaths)
