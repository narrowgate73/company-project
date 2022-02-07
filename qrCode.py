import sys
import threading
import time
import math
import cv2
import pyzbar.pyzbar as pyzbar
from PyQt5.uic.uiparser import QtCore
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT
from matplotlib.figure import Figure
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


form_class = uic.loadUiType("QR_code.ui")[0]

class MainWindow(QMainWindow, form_class):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()
        
    def initUI(self):
        
        self.pb_camOn.clicked.connect(self.start)
        self.pb_camOff.clicked.connect(self.stop)
        
    def video(self):
        #print(dtype(running))
        global running
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        
        while running:
            self.ret, self.frame = self.cap.read()
            
            if self.ret:
                #self.frame = self.read_qrcode
                self.read_qrcode()
                #print(self.frame)
                self.frame = cv2.resize(self.frame, dsize=(640, 480), interpolation=cv2.INTER_AREA)
                self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                qframe = QImage(self.frame, self.frame.shape[1], self.frame.shape[0], QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(qframe)
                self.lb_video.setPixmap(pixmap)
                
        self.cap.release()
        self.lb_video.setPixmap(QPixmap.fromImage(QImage()))
        print("thread end")
        
    def read_qrcode(self):
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        
        self.barcodes = pyzbar.decode(self.frame)
        
        for self.barcode in self.barcodes:
            
            self.x, self.y, self.w, self.h = self.barcode.rect
            self.barcode_info = self.barcode.data.decode('utf-8')
            
            cv2.rectangle(self.frame, (self.x, self.y), (self.x + self.w, self.y + self.h), (0, 0, 255), 2)
            
            cv2.putText(self.frame, self.barcode_info, (self.x, self.y - 20), self.font, 0.5, (0, 0, 255), 1)
            
        
        
        
    def start(self):
        global running 
        running = True
        th = threading.Thread(target=self.video)
        th.start()
        print("Start")
        
    def stop(self):
        global running
        running = False
        print("Stop")
              
        
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
running = False