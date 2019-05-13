from PyQt5.QtCore import QObject, pyqtSignal

class Model(QObject):
    #distance_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._directory = ''
        self._theme = ''
        self._task = ''
        self._tokens = list(list())
        self._active_distance = 0
        self._distance = []

    def setDirectory(self, value):
        self._directory = value

    def getDirectory(self):
        return self._directory

    def setTheme(self, value):
        self._theme = value

    def getTheme(self):
        return self._theme

    def setTask(self, value):
        self._task = value

    def getTask(self):
        return self._task

    def setTokens(self, value):
        self._tokens = value

    def getTokens(self):
        return self._tokens

    def setActiveDistance(self, value):
        self._active_distance = value

    def getActiveDistance(self):
        return self._active_distance

    def setDistance(self, value):
        self._distance = value

    def getDistance(self):
        return self._distance

'''
    @property
    def directory(self):
        return self._directory

    @directory.setter
    def directory(self, value):
        self._directory = value
        self.directory_changed.emit(value)
'''
