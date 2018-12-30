from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import  QThread
import datetime,  time
import serial
value = 0

class Controller(QThread, object):
    
    now = datetime.datetime.now()
    timeInterval="%0.2d:%0.2d:%0.2d" % (now.hour, now.minute, now.second)
        
    newTime = pyqtSignal(object)
    def __init__(self,  event):
        QThread.__init__(self)
        self.stopped = event

    def run(self):
        while not self.stopped.wait(1):   
            self.inTime1()
            
    def inTime1(self):
        global timeInterval
        now = datetime.datetime.now()
        timeInterval="%0.2d:%0.2d:%0.2d" % (now.hour, now.minute, now.second)

        self.newTime.emit(timeInterval)        
        
class ControlArduino(QThread):

    newValue = pyqtSignal( object , object)
    testRS232 = pyqtSignal(object)
    
    def __init__(self,  event):
        QThread.__init__(self)
        self.stopped = event
        self.altValue = 0

        
    def run(self):
        try:
            self.serArduino = serial.Serial('COM6', 115200, timeout=0) #Windows PC
            #ui.serArduino = serial.Serial("/dev/ttyACM0",115200,timeout=1)       #Linux PC - Raspberry
            self.noRS232_UNO = 1
            self.testRS232.emit( 1) 
        except:
            print ("RS232 for Arduino not found")
            self.noRS232_UNO = 0
            self.testRS232.emit(0)         

        while not self.stopped.wait(0.1):    #1 max 0.3
            self.ArduinoLoop()
            
    def ArduinoLoop(self):
        global value
        if self.noRS232_UNO: 
            self.serArduino.write(b'p')
            time.sleep(0.01)
            wert = self.serArduino.read(5)
            try:
                wert1 = wert.split()
                intwert = int(wert1[0])
                value = int(22 + (intwert/3.84))
                self.newValue.emit( intwert ,  value) 
                 
                print(intwert)
            except:
                print("error Arduino Serial")

       
          
