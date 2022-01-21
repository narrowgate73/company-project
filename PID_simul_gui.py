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

form_class = uic.loadUiType("PID_Simulation.ui")[0]

class MainWindow(QMainWindow, form_class):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()
        
    def initUI(self):
        
        self.pid_input.clicked.connect(self.inComp)
        self.pb_show.clicked.connect(self.pid_calc)
        #self.pb_clear.clicked.connect(self.logClear)
        
        self.fig = plt.figure()
        self.canvasMain = FigureCanvas(self.fig)
        self.graph.addWidget(self.canvasMain)
        #self.cmb_contType.currentIndexChanged.connect(self.cmbSet)
        
    def cmbSet(self):
        print(self.cmb_contType.currentIndex())
        
    def inComp(self):
        
        self.u_2 = self.y_1 = 0
        self.err_3 = self.err_2 = self.err_1 = 0
        self.sum_y = 0
        self.id_plt = []
        self.plant_plt = []
        self.mv_plt = []
        #self.disp_id = []
        
        self.kp_val = self.kp_input.text()
        self.ki_val = self.ki_input.text()
        self.kd_val = self.kd_input.text()
        self.sp_val = self.sp_input.text()
        
        self.kp_val = float(self.kp_val)
        self.ki_val = float(self.ki_val)
        self.kd_val = float(self.kd_val)
        self.sp_val = float(self.sp_val)
        
        self.contType = self.cmb_contType.currentIndex()
        
        print("Kp : {} | Ki : {} | kd : {}".format(self.kp_val, self.ki_val, self.kd_val))
        print(self.contType)
        print(self.sp_val)
        
        
        
        
        
        
    def logClear(self):
        
        self.disp_log.clear()
        
    def pid_calc(self):
        
        for i in range(1, 200, 1):
            
            if self.contType == 1:
                self.u_1 = self.u_2 + self.kp_val * (self.err_1 - self.err_2) + self.ki_val * self.err_1 + self.kd_val * (self.err_1 - 2 * self.err_2 + self.err_3)
                self.y_0 = 0.77 * self.y_1 + 0.322 * self.u_1 + 0.111 * self.u_2
                #self.y_0 = 1 * self.y_1 + 1 * self.u_1 + 1 * self.u_2
                self.err = self.sp_val - self.y_0
                self.py = self.y_0
                
            if i == 100:
                self.y_0 = self.y_0 * 1.5 #// 외란인가 //
                
            self.err_3 = self.err_2
            self.err_2 = self.err_1
            self.err_1 = self.err
            self.u_2 = self.u_1
            self.y_1 = self.y_0
            
            print("횟수:", i, "목표값:", self.sp_val, "제어기기출력:", self.u_1, "플랜트 출력:", self.y_0)
            
            self.id_plt.append(i)
            self.plant_plt.append(self.y_0)
            self.mv_plt.append(self.u_1)
            
            self.disp_id = str(i)
            self.disp_plant_plt = str(self.y_0)
            self.disp_mv_plt = str (self.u_1)
            self.disp_log = str(self.disp_plant_plt + self.disp_mv_plt)
            
            #self.disp_log.insertItem(self.id+plt, self.disp_log)
            #self.disp_log.insertItem(i, self.disp_plant_plt)
            #print(self.disp_plant_plt)
            
        plt.cla()
        plt.plot(self.id_plt, self.plant_plt)
        plt.plot(self.id_plt, self.mv_plt)
        plt.grid(True)
        self.canvasMain.draw()
        
                
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()