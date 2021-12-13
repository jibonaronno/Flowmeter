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
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QPushButton, QListWidget, QListWidgetItem

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

from dispatchers import PrimaryThread

from mimic import Mimic
from crud import CRUD
from dataview import DataView
from datetime import datetime

''' 
Database codes are in crud.py file. here the object name is db. Accessed by self.db.
Implemented in sensordata(...) callback function. database file is flow.db . 
'''

_UI = join(dirname(abspath(__file__)), 'top.ui')
_UI2 = join(dirname(abspath(__file__)), 'dashboard.ui')
_UI3 = join(dirname(abspath(__file__)), 'commands.ui')

#08  04  00  00  00  02  71  52
_CMD_1 = [0x08, 0x04, 0x00, 0x00, 0x00, 0x02, 0x71, 0x52]
_CMD_2 = [0x08, 0x04, 0x00, 0x00, 0x00, 0x02, 0x71, 0x52]
_CMD_3 = [0x08, 0x04, 0x00, 0x22, 0x00, 0x02, 0xD1, 0x58]
_CMD_4 = [0x08, 0x04, 0x00, 0x04, 0x00, 0x02, 0x30, 0x93]
class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.widget = uic.loadUi(_UI, self)
        self.mimic = Mimic()
        self.window_title = "top"
        self.mimic = Mimic()
        self.ports = DetectDevices()
        self.selectedPort = ""
        self.lst = QListWidget()

        self.sensor = ''
        self.sensorThread = ''
        self.sensorThreadCreated = False
        self.sensorPortOpen = False
        self.sensorDataString = ""

        self.serialSensor = ""
        self.selectedPort = ""

        self.cmdlist = []
        self.cmdlist.append(_CMD_1)
        self.cmdlist.append(_CMD_2)
        self.cmdlist.append(_CMD_3)
        self.cmdlist.append(_CMD_4)


        #List only usb-ttl ports in self.portListBox QListWidget
        self.ports = list(port_list.comports())
        for p in self.ports:
            if "USB" in p[1]:
                self.portListBox.addItem(p[0])

        self.btn1.setEnabled(False)
        self.btn2.setEnabled(True)

        #self.lst.selectedItems()
        # getting item changed signal
        self.portListBox.currentItemChanged.connect(self.portLstItemChanged)

        self.db = CRUD("flow.db")
        self.db.openDBHard()

        self.dtv = DataView()

        # renderer =  QtSvg.QSvgRenderer('ico1.svg')
        # painter = QPainter(self.btn1)
        # painter.restore()
        # renderer.render(painter)
        # self.btn1.show()

    def portLstItemChanged(self, tm):
            print("Port Item Changed " + tm.text())
            self.selectedPort = tm.text()
            if tm.text() != "":
                #if "USB" in tm.text():
                self.btn1.setEnabled(True)

    def startSensorThread(self):
        if self.sensorPortOpen:
            if not self.sensorThreadCreated:
                self.sensor = PrimaryThread(self.serialSensor, self.cmdlist)
                self.sensorThread = QThread()
                self.sensorThread.started.connect(self.sensor.run)
                self.sensor.signal.connect(self.sensorData)
                self.sensor.moveToThread(self.sensorThread)
                self.sensorThread.start()
                self.sensorThreadCreated = True
                print("Starting Sensor Thread")

    def extractData(self, starData=""):
        parts = starData.split(" ")
        res = "0000.00"
        if(len(parts) > 18):
            val = int('0x' + parts[15]+parts[16]+parts[17]+parts[18], base=16)
            res = str(val/10)
        return res

    def sensorData(self, data_stream):
        self.sensorDataString = data_stream
        strdatetime = datetime.today().strftime('%m-%d-%Y %H:%M:%S')                #Collect Present Date Time
        print(strdatetime + " - " +self.sensorDataString)                           #
        self.msgListBox.addItem(strdatetime + " - " +self.sensorDataString)         #Insert incomming data to local List Box
        self.db.insert_meter_data([strdatetime, self.sensorDataString, '0x001'])    #Inserting data to database
        if(self.msgListBox.count() > 10):
            self.msgListBox.clear()
            self.mimic.meterFlow1 = self.extractData(self.sensorDataString)

    @Slot()
    def on_btn1_clicked(self):
        if self.selectedPort != "":
            if not self.sensorPortOpen:
                try:
                    self.serialSensor = serial.Serial(self.selectedPort, baudrate=9600, timeout=0)
                    self.sensorPortOpen = True
                except serial.SerialException as ex:
                    self.sensorPortOpen = False
                    print(ex.strerror)
                    print("Error Opening Serial Port..........................................")
                finally:
                    print("Serial Port Connected..........................")
                    self.btn2.setEnabled(True)
        # self.mim = Mimic()
        # self.mim.setFixedHeight(100)
        # self.VL0.addWidget(self.mim)
        # self.setWindowTitle(self.window_title)

        #Show svg file svgwidget
        #self.svgwidget = QtSvg.QSvgWidget('ico1.svg')
        #comment self.VL1 = QVBoxLayout()
        #self.VL0.addWidget(self.svgwidget)
        #comment self.dash.show()

    @Slot()
    def on_btn2_clicked(self):
        #self.mimic.show()
        if self.sensorPortOpen:
            if not self.sensorThreadCreated:
                self.startSensorThread()
                self.mimic.show()

    @Slot()
    def on_btn3_clicked(self):
        ''' Example code to insert data in database
        #self.db.insert_meter_data_hard()
        '''


    @Slot()
    def on_btn4_clicked(self):
        self.dtv.showNormal()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    #qtmodern.styles.dark(app)
    qtmodern.styles.light(app)

    mw_class_instance = MainWindow()
    mw = qtmodern.windows.ModernWindow(mw_class_instance)
    #mw.showFullScreen()
    mw.showNormal()
    sys.exit(app.exec_())
