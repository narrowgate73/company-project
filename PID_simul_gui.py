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
        self.pb_textClear.clicked.connect(self.textClear)
        
        self.rb_type1.clicked.connect(self.outSelect)
        self.rb_type2.clicked.connect(self.outSelect)
        self.rb_type3.clicked.connect(self.outSelect)
        
        self.fig = plt.figure()
        self.canvasMain = FigureCanvas(self.fig)
        self.graph.addWidget(self.canvasMain)
        #self.cmb_contType.currentIndexChanged.connect(self.cmbSet)
        
    def cmbSet(self):
        print(self.cmb_contType.currentIndex())
        
    def outSelect(self):
        
        if self.rb_type1.isChecked():
            self.outType = 1
        elif self.rb_type2.isChecked():
            self.outType = 2
        elif self.rb_type3.isChecked():
            self.outType =3      
        
    def inComp(self):
        
        self.u_2 = self.y_1 = 0
        self.err_3 = self.err_2 = self.err_1 = 0
        self.sum_y = 0
        self.id_plt = []
        self.plant_plt = []
        self.mv_plt = []
        #self.disp_id = []
        
        self.kp_val_s = self.kp_input.text()
        self.ki_val_s = self.ki_input.text()
        self.kd_val_s = self.kd_input.text()
        self.sp_val_s = self.sp_input.text()
        
        self.outType_s = str(self.outType)
        
        self.kp_val = float(self.kp_val_s)
        self.ki_val = float(self.ki_val_s)
        self.kd_val = float(self.kd_val_s)
        self.sp_val = float(self.sp_val_s)
        
        self.contType = self.cmb_contType.currentIndex()
        
        self.textEdit.append("입력값 \n Kp : {} | Ki : {} | kd : {}  | 목표값 : {}".format(self.kp_val_s, self.ki_val_s, self.kd_val_s, self.sp_val_s))
        self.textEdit.append("제어기 출력 Type{}이 선택되었습니다".format(self.outType_s))
        
        print("Kp : {} | Ki : {} | kd : {}".format(self.kp_val, self.ki_val, self.kd_val))
        print(self.contType)
        print(self.sp_val)
        
        
        
        
        
        
    def textClear(self):
        
        self.textEdit.clear()
        
    def pid_calc(self):
        
        for i in range(1, 200, 1):
            
            if self.contType == 1:
                self.u_1 = self.u_2 + self.kp_val * (self.err_1 - self.err_2) + self.ki_val * self.err_1 + self.kd_val * (self.err_1 - 2 * self.err_2 + self.err_3)
                if self.outType == 1:
                    self.y_0 = 0.5 * self.u_1
                    
                elif self.outType == 2:
                     self.y_0 = 1 * self.y_1 + 1 * self.u_1 + 1 * self.u_2
                     
                elif self.outType == 3:
                    self.y_0 = 0.77 * self.y_1 + 0.322 * self.u_1 + 0.111 * self.u_2
                
                
                self.err = self.sp_val - self.y_0
                self.py = self.y_0
                
            if i == 100:
                self.y_0 = self.y_0 * 1.5 #// 외란인가 //
                
            self.err_3 = self.err_2
            self.err_2 = self.err_1
            self.err_1 = self.err
            self.u_2 = self.u_1
            self.y_1 = self.y_0
            
            self.id_plt.append(i)
            self.plant_plt.append(self.y_0)
            self.mv_plt.append(self.u_1)
            
            self.textEdit.append("[{}]  목표값 : {} | 제어출력 : {} | 플랜트출력 : {}".format(i, self.sp_val, self.u_1, self.y_0))
            
        plt.cla()
        plt.plot(self.id_plt, self.plant_plt)
        plt.plot(self.id_plt, self.mv_plt)
        plt.grid(True)
        self.canvasMain.draw()
        
                
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()