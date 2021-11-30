#!/usr/bin/python3
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Mimic(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()
        #self.show()

    def initUI(self):
        self.text = "hello world"
        self.setGeometry(0, 0, 800, 600)
        self.setWindowTitle('Draw Demo')

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        qp.setPen(QColor(Qt.red))
        qp.setFont(QFont('Arial', 20))
        qp.drawText(10, 50, "hello Python")
        qp.setPen(QColor(Qt.blue))
        qp.drawLine(10, 100, 100, 100)
        qp.drawRect(10, 150, 150, 100)
        qp.setPen(QColor(Qt.yellow))
        qp.drawEllipse(100, 50, 100, 50)
        qp.drawPixmap(220, 10, QPixmap("pythonlogo.png"))
        qp.fillRect(20, 175, 130, 70, QBrush(Qt.SolidPattern))
        qp.end()