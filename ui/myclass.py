
from PyQt5.QtWidgets import QApplication
from ui.mainWindow import MainWindow
import sys
import datetime
from threading import Event
from PyQt5.QtWidgets import   QGraphicsView
from PyQt5 import QtWidgets
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import pyqtSignal
from mainWindow import MainWindow

class Controller(QThread):
    my_signal = pyqtSignal()
    def __init__(self,  event):
        QThread.__init__(self)
        self.stopped = event

    def run(self):
        while not self.stopped.wait(1):   
            self.inTime1()
            
            #ui.item.setRotation(100)
            
    def inTime1(self):
        now = datetime.datetime.now()
        timeInterval="%0.2d:%0.2d:%0.2d" % (now.hour, now.minute, now.second)
        ui.lbltime.setText(timeInterval)
        ui.my_signal.emit()
