
from os.path import join, dirname, abspath
from qtpy import uic
from qtpy.QtCore import Slot, QTimer, QThread, Signal, QObject, Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

_UI3 = join(dirname(abspath(__file__)), 'dataview.ui')

class DataView(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self)  # self, *args, **kwargs
        self.setParent(parent)
        self.widget = uic.loadUi(_UI3, self)
        self.initUI()

    def initUI(self):
        pass