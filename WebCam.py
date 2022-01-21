import sys
import time
import math
from PyQt5 import QtGui
import cv2
import threading
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

form_class = uic.loadUiType("project_01.ui")[0]

class Mainwindow(QMainWindow, form_class):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()
        running = False
        
    def initUI(self):
        
        
        
        self.pb_camOn.clicked.connect(self.start)
        self.pb_camOff.clicked.connect(self.stop)
        self.pb_shot.clicked.connect(self.shot)
        
    def run(self):
        global running 
        self.cap = cv2.VideoCapture(0) 
        
        while running:
            self.lb_picture.setPixmap(QPixmap.fromImage(QImage()))
            self.lb_edge.setPixmap(QPixmap.fromImage(QImage()))
            self.ret, self.img = self.cap.read()
            if self.ret:
                #self.img = cv2.resize(self.img, None, fx=0.7, fy=0.7, interpolation=cv2.INTER_AREA)
                self.img = cv2.resize(self.img, dsize=(640, 480), interpolation=cv2.INTER_AREA)
                self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
                qImg = QImage(self.img, self.img.shape[1], self.img.shape[0], QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(qImg)
                self.lb_photo.setPixmap(pixmap)
                
        self.cap.release()
        self.lb_photo.setPixmap(QPixmap.fromImage(QImage()))
        print("thread end")
        
    def start(self):
        global running 
        running = True
        th = threading.Thread(target=self.run)
        th.start()
        print("start")
        
    def stop(self):
        global running
        running = False
        
        print('stop')
        
    def shot(self):
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        self.img = cv2.resize(self.img, dsize=(320, 240), interpolation=cv2.INTER_AREA)
        self.img_norm = cv2.normalize(self.img, None, 0, 255, cv2.NORM_MINMAX)
        cv2.imwrite("test_01.jpg", self.img_norm)
        self.stop()
        
        self.edges = cv2.Canny(self.img, 100, 200)
        self.cannyImg = QtGui.QImage(self.edges.data, self.edges.shape[1], self.edges.shape[0], QtGui.QImage.Format_Grayscale8)
        
        self.loadImg = QPixmap()
        self.loadImg.load("test_01.jpg")
        self.lb_picture.setPixmap(self.loadImg)
        
        qPix_canny = QPixmap.fromImage(self.cannyImg)
        self.lb_edge.setPixmap(qPix_canny)
        
        print("shot")
        
                
            

app = QApplication(sys.argv)
window = Mainwindow()
window.show()
app.exec_()    
running = False