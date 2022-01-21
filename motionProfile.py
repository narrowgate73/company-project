import sys
import time
import math
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

form_class = uic.loadUiType("profile.ui")[0]

class Mainwindow(QMainWindow, form_class):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()
        
    def initUI(self):
        self.pb_inComp.clicked.connect(self.inComp)
        self.pb_linear.clicked.connect(self.trapezodial)
        self.pb_Scurve.clicked.connect(self.sCurve)
        
        self.disp_vm = QLCDNumber(self)
        self.disp_vm.move(120, 150)
        self.disp_vm.resize(140, 30)
        
        self.disp_Svm = QLCDNumber(self)
        self.disp_Svm.move(530, 150)
        self.disp_Svm.resize(140, 30)
        
        self.fig = plt.figure()
        
        self.canvas01 = FigureCanvas(self.fig)
        self.gp_linear.addWidget(self.canvas01)
        
        self.canvas02 = FigureCanvas(self.fig)
        self.gp_sCurve.addWidget(self.canvas02)
        
        self.canvas03 = FigureCanvas(self.fig)
        self.nd_linear.addWidget(self.canvas03)
        
        self.canvas04 = FigureCanvas(self.fig)
        self.nd_sCurve.addWidget(self.canvas04)
        
    def inComp(self):
    
        #common
        self.accTime = self.input_accTime.text()
        self.decTime = self.input_decTime.text()
        self.moveTime = self.input_moveTime.text()
        self.distance = self.input_distance.text()
        
        self.accTime = float(self.accTime)
        self.decTime = float(self.decTime)
        self.moveTime = float(self.moveTime)
        self.distance = (float(self.distance))
        self.constTime = float(self.moveTime - self.accTime - self.decTime)
        
        self.t1 = self.accTime
        self.t2 = self.moveTime - self.decTime
        self.t3 = self.moveTime
        
        
        
        #Trapezodial
        self.T_vm = ((2 * self.distance) / ((-self.t1) + self.t2 + self.t3))
        self.acc = self.T_vm / self.accTime
        self.dec = abs(self.T_vm / self.decTime)
        
        self.disp_vm.display(self.T_vm) 
        
        #S-Curve
        
        self.S_vm = round((2 * self.distance) / (self.accTime + (2 * self.constTime) + self.decTime), 4)
        self.d_acc = round(self.accTime * self.S_vm / 2, 2)
        self.d_const = round(self.constTime * self.S_vm, 2)
        self.d_dec = round(self.decTime * self.S_vm / 2, 2)
        
        self.disp_Svm.display(self.S_vm)
        
    def trapezodial(self):
        targetPos = self.distance
        maxVel = self.T_vm
        moveTime = self.moveTime
        ts = 0.001
        t = np.arange(0, moveTime, ts)
        acc = self.acc
        dec = self.dec
        
        
        posRef = np.zeros(shape=(t.size, ))
        velRef = np.zeros(shape=(t.size, ))
        tmp = np.zeros(shape=(1, t.size))
        
        for i in range(1, t.size):
            if targetPos >= posRef[i-1]:
                
                velRef[i] = min([velRef[i-1] + acc * ts, maxVel, np.sqrt(2 * dec * np.abs(targetPos - posRef[i-1]))])
                
            elif targetPos < posRef[i-1]:
                
                velRef[i] = max([velRef[i-1] - acc * ts, -maxVel, -np.sqrt(2 * acc * np.abs(targetPos - posRef[i-1]))])
                
            posRef[i] = posRef[i-1] + velRef[i] *ts
        
        plt.cla()
        plt.plot(t, posRef, 'g', t, velRef, 'r')
        plt.grid(True)
        self.canvas01.draw()
    
    
    def sCurve(self):
        targetPos = self.distance
        maxVel = self.S_vm
        moveTime = self.moveTime
        
        ts = 0.001
        
        t = np.arange(0, self.moveTime, ts)
        
        posRef = np.zeros(shape=(t.size, ))
        velRef = np.zeros(shape=(t.size, ))
        tmp = np.zeros(shape=(1, t.size))
        
        for i in range(0, t.size):
            if self.accTime >= t[i]:
                velRef[i] = self.d_acc * ((1 / self.accTime) - (1 / self.accTime) * math.cos(math.pi * t[i] / self.accTime))
                posRef[i] = self.d_acc * ((t[i] / self.accTime) - (1 / math.pi) * math.sin(math.pi * t[i] / self.accTime))
                
            elif self.accTime + self.constTime >= t[i]:
                velRef[i] = self.S_vm
                posRef[i] = posRef[i-1] + velRef[i] *ts
                
            elif self.accTime + self.constTime < t[i]:
                offset = np.round(self.accTime + self.constTime, 4)
                velRef[i] = self.d_dec * ((1 / self.decTime) + (1 / self.decTime) * math.cos(math.pi * (t[i] - offset) / self.decTime))
                posRef[i] = posRef[i-1] + velRef[i] *ts
                
        plt.cla()
        plt.plot(t, posRef, 'g', t, velRef, 'r')
        plt.grid(True)
        self.canvas02.draw()
        
        #sCurve_Vmean = np.mean(velRef)
        #sCurve_Vvar = np.var(velRef)
        #sCurve_Vstd = np.std(velRef)
        #sCurve_Pmean = np.mean(posRef)
        #sCurve_Pvar = np.var(posRef)
        #sCurve_Pstd = np.std(posRef)
        
        #plt.cla()
        #plt.plot(t, np.mean, t, np.var,t, np.std)
        #plt.grid(True)
        #self.canvas04.draw()
                   
    
app = QApplication(sys.argv)
window = Mainwindow()
window.show()
app.exec_()