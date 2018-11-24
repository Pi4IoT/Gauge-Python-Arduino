# -*- coding: utf-8 -*-
import sys

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow

from .Ui_mainWindow import Ui_MainWindow

from PyQt5 import QtWidgets
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QPen,  QPixmap

from PyQt5.QtCore import  Qt
from threading import Event

from newValue import Controller,  ControlArduino

ICON_RED_LED = "icons/led-red-on.png"
ICON_GREEN_LED = "icons/green-led-on.png"       
        
class MainWindow(QMainWindow, Ui_MainWindow):
    
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        
        pen = QPen(Qt.red)
        pen.setWidth(3)
        pen.setCapStyle(Qt.RoundCap)    
        scene = QtWidgets.QGraphicsScene()
        pen.setCosmetic(True)  
        scene.addPixmap(QPixmap('back.png'))
        self.item = scene.addLine(60, 170, 97, 97, pen)   
        pen = QtGui.QPen(QtGui.QColor(QtCore.Qt.gray))
        brush = QtGui.QBrush(pen.color().darker(100))
        scene.addEllipse(87, 87, 20, 20, pen, brush)
        self.item.setTransformOriginPoint(97, 97)
        self.Grafik.setScene(scene)

        self.stop_flag_time =  Event()
        self.stop_flag_RS232 =  Event()

        self.getController = Controller(self.stop_flag_time)
        self.getController.start()
        self.getController.newTime.connect(self.updateTime)
 
        self.getArduino = ControlArduino(self.stop_flag_RS232)
        self.getArduino.newValue.connect(self.updatePoti)  
        self.getArduino.testRS232.connect(self.updateInfoRS232)          
        self.getArduino.start() 
        
    @pyqtSlot()
    def on_btnExit_clicked(self):
        self.stop_flag_time.set()
        self.stop_flag_RS232.set()
        sys.exit(0);

    def updateTime(self,  timeInterval):
        self.lbltime.setText(timeInterval)

    def updatePoti(self, poti,  potiRotation):
        self.lblAnzeige.setText(str(poti))
        self.item.setRotation(potiRotation)
        
    def updateInfoRS232(self, rs232):
        print(rs232)
        if rs232:
            self.lblStatusLedUNORS232.setPixmap(QtGui.QPixmap(ICON_GREEN_LED))
            self.lblRSinfo.setText("Arduino RS232 okay")
        else:
            self.lblStatusLedUNORS232.setPixmap(QtGui.QPixmap(ICON_RED_LED))
            self.lblRSinfo.setText("Arduino RS232 failed")
            self.lblAnzeige.setText("Error")
            self.stop_flag_RS232.set()
