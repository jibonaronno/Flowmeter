#!/usr/bin/python3
import sys
import enum
from os.path import join, dirname, abspath
import queue
import serial
import serial.tools.list_ports as port_list
from qtpy import uic
from qtpy.QtCore import Slot, QTimer, QThread, Signal, QObject, Qt
from qtpy.QtWidgets import QApplication, QMainWindow, QMessageBox, QAction, QDialog, QTableWidgetItem, QLabel
from pyqtgraph import PlotWidget
import pyqtgraph as pg
from collections import deque
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtGui import QPainter
from PyQt5 import QtCore, QtSvg
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QPushButton

import math
import os
import numpy as np
import random
import qtmodern.styles
import qtmodern.windows
import time
import json
import pprint
from portdetection import DetectDevices

_UI = join(dirname(abspath(__file__)), 'top.ui')

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.widget = uic.loadUi(_UI, self)
        window_title = "top"
        self.setWindowTitle(window_title)
        self.svgwidget = QtSvg.QSvgWidget('ico1.svg')
        #self.VL1 = QVBoxLayout()
        self.VL0.addWidget(self.svgwidget)

        renderer =  QtSvg.QSvgRenderer('ico1.svg')
        painter = QPainter(self.btn1)
        painter.restore()
        renderer.render(painter)
        self.btn1.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    #qtmodern.styles.dark(app)
    qtmodern.styles.light(app)

    mw_class_instance = MainWindow()
    mw = qtmodern.windows.ModernWindow(mw_class_instance)
    #mw.showFullScreen()
    mw.showNormal()
    sys.exit(app.exec_())
