import sys
from PySide2 import QtCore, QtWidgets
from modules.equalizer_bar import EqualizerBar

import random


class Window(QtWidgets.QMainWindow):

    def __init__(self, color):
        super().__init__()

        self.equalizer = EqualizerBar(5, [color for i in range(5)])
        self.setCentralWidget(self.equalizer)

        self._timer = QtCore.QTimer()
        self._timer.setInterval(100)
        self._timer.timeout.connect(self.update_values)
        self._timer.start()

    def update_values(self):
        self.equalizer.setValues([
            min(100, v+random.randint(0, 50) if random.randint(0, 5) > 2 else v)
            for v in self.equalizer.values()
            ])


class Visualizer:
    def __init__(self):
        print("Initializing visualizer...")
    
    def show(self, color):
        app = None
        if not QtWidgets.QApplication.instance():
            app = QtWidgets.QApplication(sys.argv)
        else:
            app = QtWidgets.QApplication.instance()
        w = Window(color)
        w.show()
        app.exec_()





