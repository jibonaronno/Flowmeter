
from os.path import join, dirname, abspath
from qtpy import uic
from qtpy.QtCore import Slot, QTimer, QThread, Signal, QObject, Qt
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from crud import CRUD

_UI3 = join(dirname(abspath(__file__)), 'dataview.ui')

class DataView(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self)  # self, *args, **kwargs
        self.setParent(parent)
        self.widget = uic.loadUi(_UI3, self)
        self.startdte = QDateTimeEdit()
        self.crud = CRUD("flow.db")
        self.crud.openDBHard()
        self.initUI()
        #self.tableWidget = QTableWidget()


    def initUI(self):
        self.startdte = self.startDate
        self.startdte.setDateTime(QtCore.QDateTime.currentDateTime())
        self.stopDate.setDateTime(QtCore.QDateTime.currentDateTime())

    @Slot()
    def on_btnQuery_clicked(self):
        idx = 0
        data = self.crud.getListByDateRange(self.startdte.dateTime(), self.stopDate.dateTime())
        print(len(data))
        #print(data[0])
        self.tableWidget.clear()
        self.tableWidget.setRowCount(len(data))
        for dat in data:
            self.tableWidget.setItem(idx, 0, QTableWidgetItem(dat[0]))
            self.tableWidget.setItem(idx, 1, QTableWidgetItem(dat[1]))
            self.tableWidget.setItem(idx, 2, QTableWidgetItem(dat[2]))
            self.tableWidget.setItem(idx, 3, QTableWidgetItem(dat[3]))
            idx += 1
