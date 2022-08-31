import random
import time
import sys

from PyQt5.QtWidgets import QApplication, QCheckBox, QRadioButton
from PyQt5.QtWidgets import QLabel, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QTextEdit, QPushButton, QGridLayout
from PyQt5.QtCore import pyqtSignal, QObject, Qt
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg

from paho.mqtt import client as mqtt_client
import numpy as np
import json

connected=False
broker_address="front.dii.unitn.it"
port=10883
user="keizer"
password="tryingtoiot"
topic1 = "/cabinet/"
client_id = "MQTT1"

bufaccx = {'1':np.zeros(100,dtype='float'),'2':np.zeros(100,dtype='float'),'3':np.zeros(100,dtype='float'),'4':np.zeros(100,dtype='float'),'5':np.zeros(100,dtype='float')}
bufposx = {'1':np.zeros(2,dtype='float'),'2':np.zeros(2,dtype='float'),'3':np.zeros(2,dtype='float'),'4':np.zeros(2,dtype='float'),'5':np.zeros(2,dtype='float')}
bufaccy = {'1':np.zeros(100,dtype='float'),'2':np.zeros(100,dtype='float'),'3':np.zeros(100,dtype='float'),'4':np.zeros(100,dtype='float'),'5':np.zeros(100,dtype='float')}
bufposy = {'1':np.zeros(2,dtype='float'),'2':np.zeros(2,dtype='float'),'3':np.zeros(2,dtype='float'),'4':np.zeros(2,dtype='float'),'5':np.zeros(2,dtype='float')}
bufaccz = {'1':np.zeros(100,dtype='float'),'2':np.zeros(100,dtype='float'),'3':np.zeros(100,dtype='float'),'4':np.zeros(100,dtype='float'),'5':np.zeros(100,dtype='float')}

iacx = 0
iacy = 0
iacz = 0
iposx = 0
iposy = 0
retarr = np.empty(20)

class CustomPlot1(pg.PlotWidget):
    def __init__(self):
        pg.PlotWidget.__init__(self)
        self.plotItem.setTitle("Acceleration X-axis")
        self.x = list(range(100))  # 100 time points
        self.f1 = retarr[0]
        self.f2 = retarr[1]
        self.f3 = retarr[2]
        self.f4 = retarr[3]
        self.f5 = retarr[4]
        if self.f1 == 1:
            self.y1 = list(bufaccx['1'])
            self.data_line1 = self.plot(self.x, self.y1, pen='g', symbol='o', symbolPen='g', symbolSize=1)
            self.timer1 = QtCore.QTimer()
            self.timer1.setInterval(60)
            self.timer1.timeout.connect(lambda:self.redraw('1'))
            self.timer1.start()
        else:
            try:
                pass
            except NameError:
                pass 
        if self.f2 == 1:
            self.y2 = list(bufaccx['2'])
            self.data_line2 = self.plot(self.x, self.y2, pen='r', symbol='o', symbolPen='g', symbolSize=1)
            self.timer2 = QtCore.QTimer()
            self.timer2.setInterval(60)
            self.timer2.timeout.connect(lambda:self.redraw('2'))
            self.timer2.start()
        else:
            try:
                pass
            except NameError:
                pass 
        if self.f3 == 1:
            self.y3 = list(bufaccx['3'])
            self.data_line3 = self.plot(self.x, self.y3, pen='b', symbol='o', symbolPen='g', symbolSize=1)
            self.timer3 = QtCore.QTimer()
            self.timer3.setInterval(60)
            self.timer3.timeout.connect(lambda:self.redraw('3'))
            self.timer3.start()
        else:
            try:
                pass
            except NameError:
                pass 
        if self.f4 == 1:
            self.y4 = list(bufaccx['4'])
            self.data_line4 = self.plot(self.x, self.y4, pen='y', symbol='o', symbolPen='g', symbolSize=1)
            self.timer4 = QtCore.QTimer()
            self.timer4.setInterval(60)
            self.timer4.timeout.connect(lambda:self.redraw('4'))
            self.timer4.start()
        else:
            try:
                pass
            except NameError:
                pass 
        if self.f5 == 1:
            self.y5 = list(bufaccx['5'])
            self.data_line5 = self.plot(self.x, self.y5, pen='w', symbol='o', symbolPen='g', symbolSize=1)
            self.timer5 = QtCore.QTimer()
            self.timer5.setInterval(60)
            self.timer5.timeout.connect(lambda:self.redraw('5'))
            self.timer5.start()
        else:
            try:
                pass
            except NameError:
                pass 

    def redraw(self, args):
        self.x = self.x[1:]  # Remove the first element.
        self.x.append(self.x[-1] + 1)  # Add a new value.
        if args == '1':
            self.y1 = self.y1[1:]  # Remove the first 

            self.y1.append(bufaccx[args][(iacx-1)%100])  # Add a new value.

            self.data_line1.setData(self.x, self.y1)  # Update the data.
        if args == '2':
            self.y2 = self.y2[1:]  # Remove the first 

            self.y2.append(bufaccx[args][(iacx-1)%100])  # Add a new value.

            self.data_line2.setData(self.x, self.y2)  # Update the data.
        if args == '3':
            self.y3 = self.y3[1:]  # Remove the first 

            self.y3.append(bufaccx[args][(iacx-1)%100])  # Add a new value.

            self.data_line3.setData(self.x, self.y3)  # Update the data.
        if args == '4':
            self.y4 = self.y4[1:]  # Remove the first 

            self.y4.append(bufaccx[args][(iacx-1)%100])  # Add a new value.

            self.data_line4.setData(self.x, self.y4)  # Update the data.
        if args == '5':
            self.y5 = self.y5[1:]  # Remove the first 

            self.y5.append(bufaccx[args][(iacx-1)%100])  # Add a new value.

            self.data_line5.setData(self.x, self.y5)  # Update the data.            

class CustomPlot2(pg.PlotWidget,QWidget):
    def __init__(self):
        pg.PlotWidget.__init__(self)
        self.plotItem.setTitle("Acceleration Y-axis")
        self.x = list(range(100))  # 100 time points
        self.f1 = retarr[5]
        self.f2 = retarr[6]
        self.f3 = retarr[7]
        self.f4 = retarr[8]
        self.f5 = retarr[9]
        if self.f1 == 1:
            self.y1 = list(bufaccy['1'])
            self.data_line1 = self.plot(self.x, self.y1, pen='g', symbol='o', symbolPen='g', symbolSize=1)
            self.timer1 = QtCore.QTimer()
            self.timer1.setInterval(60)
            self.timer1.timeout.connect(lambda:self.redraw('1'))
            self.timer1.start()
        else:
            try:
                pass
            except NameError:
                pass 
        if self.f2 == 1:
            self.y2 = list(bufaccy['2'])
            self.data_line2 = self.plot(self.x, self.y2, pen='r', symbol='o', symbolPen='g', symbolSize=1)
            self.timer2 = QtCore.QTimer()
            self.timer2.setInterval(60)
            self.timer2.timeout.connect(lambda:self.redraw('2'))
            self.timer2.start()
        else:
            try:
                pass
            except NameError:
                pass 
        if self.f3 == 1:
            self.y3 = list(bufaccy['3'])
            self.data_line3 = self.plot(self.x, self.y3, pen='b', symbol='o', symbolPen='g', symbolSize=1)
            self.timer3 = QtCore.QTimer()
            self.timer3.setInterval(60)
            self.timer3.timeout.connect(lambda:self.redraw('3'))
            self.timer3.start()
        else:
            try:
                pass
            except NameError:
                pass 
        if self.f4 == 1:
            self.y4 = list(bufaccy['4'])
            self.data_line4 = self.plot(self.x, self.y4, pen='y', symbol='o', symbolPen='g', symbolSize=1)
            self.timer4 = QtCore.QTimer()
            self.timer4.setInterval(60)
            self.timer4.timeout.connect(lambda:self.redraw('4'))
            self.timer4.start()
        else:
            try:
                pass
            except NameError:
                pass 
        if self.f5 == 1:
            self.y5 = list(bufaccy['5'])
            self.data_line5 = self.plot(self.x, self.y5, pen='w', symbol='o', symbolPen='g', symbolSize=1)
            self.timer5 = QtCore.QTimer()
            self.timer5.setInterval(60)
            self.timer5.timeout.connect(lambda:self.redraw('5'))
            self.timer5.start()
        else:
            try:
                pass
            except NameError:
                pass 

    def redraw(self, args):
        self.x = self.x[1:]  # Remove the first element.
        self.x.append(self.x[-1] + 1)  # Add a new value.
        if args == '1':
            self.y1 = self.y1[1:]  # Remove the first 

            self.y1.append(bufaccy[args][(iacy-1)%100])  # Add a new value.

            self.data_line1.setData(self.x, self.y1)  # Update the data.
        if args == '2':
            self.y2 = self.y2[1:]  # Remove the first 

            self.y2.append(bufaccy[args][(iacy-1)%100])  # Add a new value.

            self.data_line2.setData(self.x, self.y2)  # Update the data.
        if args == '3':
            self.y3 = self.y3[1:]  # Remove the first 

            self.y3.append(bufaccy[args][(iacy-1)%100])  # Add a new value.

            self.data_line3.setData(self.x, self.y3)  # Update the data.
        if args == '4':
            self.y4 = self.y4[1:]  # Remove the first 

            self.y4.append(bufaccy[args][(iacy-1)%100])  # Add a new value.

            self.data_line4.setData(self.x, self.y4)  # Update the data.
        if args == '5':
            self.y5 = self.y5[1:]  # Remove the first 

            self.y5.append(bufaccy[args][(iacy-1)%100])  # Add a new value.

            self.data_line5.setData(self.x, self.y5)  # Update the data.  

class CustomPlot3(pg.PlotWidget):
    def __init__(self):
        pg.PlotWidget.__init__(self)
        self.plotItem.setTitle("Acceleration Z-axis")
        self.x = list(range(100))  # 100 time points
        self.f1 = retarr[10]
        self.f2 = retarr[11]
        self.f3 = retarr[12]
        self.f4 = retarr[13]
        self.f5 = retarr[14]
        if self.f1 == 1:
            self.y1 = list(bufaccz['1'])
            self.data_line1 = self.plot(self.x, self.y1, pen='g', symbol='o', symbolPen='g', symbolSize=1)
            self.timer1 = QtCore.QTimer()
            self.timer1.setInterval(60)
            self.timer1.timeout.connect(lambda:self.redraw('1'))
            self.timer1.start()
        else:
            try:
                pass
            except NameError:
                pass 
        if self.f2 == 1:
            self.y2 = list(bufaccz['2'])
            self.data_line2 = self.plot(self.x, self.y2, pen='r', symbol='o', symbolPen='g', symbolSize=1)
            self.timer2 = QtCore.QTimer()
            self.timer2.setInterval(60)
            self.timer2.timeout.connect(lambda:self.redraw('2'))
            self.timer2.start()
        else:
            try:
                pass
            except NameError:
                pass 
        if self.f3 == 1:
            self.y3 = list(bufaccz['3'])
            self.data_line3 = self.plot(self.x, self.y3, pen='b', symbol='o', symbolPen='g', symbolSize=1)
            self.timer3 = QtCore.QTimer()
            self.timer3.setInterval(60)
            self.timer3.timeout.connect(lambda:self.redraw('3'))
            self.timer3.start()
        else:
            try:
                pass
            except NameError:
                pass 
        if self.f4 == 1:
            self.y4 = list(bufaccz['4'])
            self.data_line4 = self.plot(self.x, self.y4, pen='y', symbol='o', symbolPen='g', symbolSize=1)
            self.timer4 = QtCore.QTimer()
            self.timer4.setInterval(60)
            self.timer4.timeout.connect(lambda:self.redraw('4'))
            self.timer4.start()
        else:
            try:
                pass
            except NameError:
                pass 
        if self.f5 == 1:
            self.y5 = list(bufaccz['5'])
            self.data_line5 = self.plot(self.x, self.y5, pen='w', symbol='o', symbolPen='g', symbolSize=1)
            self.timer5 = QtCore.QTimer()
            self.timer5.setInterval(60)
            self.timer5.timeout.connect(lambda:self.redraw('5'))
            self.timer5.start()
        else:
            try:
                pass
            except NameError:
                pass 

    def redraw(self, args):
        self.x = self.x[1:]  # Remove the first element.
        self.x.append(self.x[-1] + 1)  # Add a new value.
        if args == '1':
            self.y1 = self.y1[1:]  # Remove the first 

            self.y1.append(bufaccz[args][(iacz-1)%100])  # Add a new value.

            self.data_line1.setData(self.x, self.y1)  # Update the data.
        if args == '2':
            self.y2 = self.y2[1:]  # Remove the first 

            self.y2.append(bufaccz[args][(iacz-1)%100])  # Add a new value.

            self.data_line2.setData(self.x, self.y2)  # Update the data.
        if args == '3':
            self.y3 = self.y3[1:]  # Remove the first 

            self.y3.append(bufaccz[args][(iacz-1)%100])  # Add a new value.

            self.data_line3.setData(self.x, self.y3)  # Update the data.
        if args == '4':
            self.y4 = self.y4[1:]  # Remove the first 

            self.y4.append(bufaccz[args][(iacz-1)%100])  # Add a new value.

            self.data_line4.setData(self.x, self.y4)  # Update the data.
        if args == '5':
            self.y5 = self.y5[1:]  # Remove the first 

            self.y5.append(bufaccz[args][(iacz-1)%100])  # Add a new value.

            self.data_line5.setData(self.x, self.y5)  # Update the data.  

class CustomPlot4(pg.ScatterPlotItem):
    def __init__(self):
        pg.ScatterPlotItem.__init__(self)
        self.f1 = retarr[15]
        self.f2 = retarr[16]
        self.f3 = retarr[17]
        self.f4 = retarr[18]
        self.f5 = retarr[19]
        self.x1 = list(bufposx['1']) 
        self.x2 = list(bufposx['2']) 
        self.x3 = list(bufposx['3']) 
        self.x4 = list(bufposx['4']) 
        self.x5 = list(bufposx['5']) 
        if self.f1 == 1:      
            self.y1 = list(bufposy['1'])
            self.data_line1 = self.setData(self.x1, self.y1,pen='g',symbol='o',size=3)
            self.timer1 = QtCore.QTimer()
            self.timer1.setInterval(60)
            self.timer1.timeout.connect(lambda:self.redraw('1'))
            self.timer1.start()
        else:
            try:
                pass
            except NameError:
                pass 
        if self.f2 == 1:       
            self.y2 = list(bufposy['2'])
            self.data_line2 = self.setData(self.x2, self.y2,pen='g',symbol='o',size=3)
            self.timer2 = QtCore.QTimer()
            self.timer2.setInterval(60)
            self.timer2.timeout.connect(lambda:self.redraw('2'))
            self.timer2.start()
        else:
            try:
                pass
            except NameError:
                pass 
        if self.f3 == 1:        
            self.y3 = list(bufposy['3'])
            self.data_line3 = self.setData(self.x3, self.y3,pen='g',symbol='o',size=3)
            self.timer3 = QtCore.QTimer()
            self.timer3.setInterval(60)
            self.timer3.timeout.connect(lambda:self.redraw('3'))
            self.timer3.start()
        else:
            try:
                pass
            except NameError:
                pass 
        if self.f4 == 1:      
            self.y4 = list(bufposy['4'])
            self.data_line4 = self.setData(self.x4, self.y4,pen='g',symbol='o',size=3)
            self.timer4 = QtCore.QTimer()
            self.timer4.setInterval(60)
            self.timer4.timeout.connect(lambda:self.redraw('4'))
            self.timer4.start()
        else:
            try:
                pass
            except NameError:
                pass 
        if self.f5 == 1:       
            self.y5 = list(bufposy['5'])
            self.data_line5 = self.setData(self.x5, self.y5,pen='g',symbol='o',size=3)
            self.timer5 = QtCore.QTimer()
            self.timer5.setInterval(60)
            self.timer5.timeout.connect(lambda:self.redraw('5'))
            self.timer5.start()
        else:
            try:
                pass
            except NameError:
                pass 

    def redraw(self, args):

        if args == '1':
            self.x1 = self.x1[1:]  # Remove the first 

            self.x1.append(bufposx[args][(iposx-1)%2])  # Add a new value.
            
            self.y1 = self.y1[1:]  # Remove the first 

            self.y1.append(bufposy[args][(iposy-1)%2])  # Add a new value.

            self.data_line1.setData(self.x1, self.y1)  # Update the data.
        if args == '2':
            self.x2 = self.x2[1:]  # Remove the first 

            self.x2.append(bufposx[args][(iposx-1)%2])  # Add a new value.
            
            self.y2 = self.y2[1:]  # Remove the first 

            self.y2.append(bufposy[args][(iposy-1)%2])  # Add a new value.

            self.data_line2.setData(self.x2, self.y2)  # Update the data.
        if args == '3':
            self.x3 = self.x3[1:]  # Remove the first 

            self.x3.append(bufposx[args][(iposx-1)%2])  # Add a new value.
            
            self.y3 = self.y3[1:]  # Remove the first 

            self.y3.append(bufposy[args][(iposy-1)%2])  # Add a new value.

            self.data_line3.setData(self.x3, self.y3)  # Update the data.
        if args == '4':
            self.x4 = self.x4[1:]  # Remove the first 

            self.x4.append(bufposx[args][(iposx-1)%2])  # Add a new value.
            
            self.y4 = self.y4[1:]  # Remove the first 

            self.y4.append(bufposy[args][(iposy-1)%2])  # Add a new value.

            self.data_line4.setData(self.x4, self.y4)  # Update the data.
        if args == '5':
            self.x5 = self.x5[1:]  # Remove the first 

            self.x5.append(bufposx[args][(iposx-1)%2])  # Add a new value.
            
            self.y5 = self.y5[1:]  # Remove the first 

            self.y5.append(bufposy[args][(iposy-1)%2])  # Add a new value.

            self.data_line5.setData(self.x5, self.y5)  # Update the data.

class Checkboxes(QWidget):
    def __init__(self,text,CustomPlot1,CustomPlot2,CustomPlot3,CustomPlot4,parent=None):
        super(Checkboxes,self).__init__(parent)
        self._create_cbx(text)
        CustomPlot1=CustomPlot1
        CustomPlot2=CustomPlot2
        CustomPlot3=CustomPlot3
        CustomPlot4=CustomPlot4
    def _create_cbx(self,text):
        self.layout = QHBoxLayout(self)
        self.cbx = QRadioButton(self)
        self.cbx.setChecked(False)
        self.cbx.setText(text)
        self.cbx.toggled.connect(lambda:callback_checkbox(self.cbx,CustomPlot1,CustomPlot2,CustomPlot3,CustomPlot4))  
        self.show()
        
def callback_checkbox(smth,CustomPlot1,CustomPlot2,CustomPlot3,CustomPlot4):
    CustomPlot1x=CustomPlot1()
    CustomPlot2x=CustomPlot2()
    CustomPlot3x=CustomPlot3()
    CustomPlot4x=CustomPlot4()
    setattr(CustomPlot1x,'f1',0)
    setattr(CustomPlot2x,'f1',0)
    setattr(CustomPlot3x,'f1',0)
    setattr(CustomPlot4x,'f1',0)
    setattr(CustomPlot1x,'f2',0)
    setattr(CustomPlot2x,'f2',0)
    setattr(CustomPlot3x,'f2',0)
    setattr(CustomPlot4x,'f2',0)
    setattr(CustomPlot1x,'f3',0)
    setattr(CustomPlot2x,'f3',0)
    setattr(CustomPlot3x,'f3',0)
    setattr(CustomPlot4x,'f3',0)
    setattr(CustomPlot1x,'f4',0)
    setattr(CustomPlot2x,'f4',0)
    setattr(CustomPlot3x,'f4',0)
    setattr(CustomPlot4x,'f4',0)
    setattr(CustomPlot1x,'f5',0)
    setattr(CustomPlot2x,'f5',0)
    setattr(CustomPlot3x,'f5',0)
    setattr(CustomPlot4x,'f5',0)
    if smth.isChecked() == True and smth.text() == "Roman":
        CustomPlot1x.f1 = 1
        CustomPlot2x.f1 = 1
        CustomPlot3x.f1 = 1
        CustomPlot4x.f1 = 1
    elif smth.isChecked() == False and smth.text() == "Roman":
        CustomPlot1x.f1 = 0
        CustomPlot2x.f1 = 0
        CustomPlot3x.f1 = 0
        CustomPlot4x.f1 = 0
    else:
        pass
    if smth.isChecked() == True and smth.text() == "Matteo":
        CustomPlot1x.f2 = 1
        CustomPlot2x.f2 = 1
        CustomPlot3x.f2 = 1
        CustomPlot4x.f2 = 1
    elif smth.isChecked() == False and smth.text() == "Matteo":
        CustomPlot1x.f2 = 0
        CustomPlot2x.f2 = 0
        CustomPlot3x.f2 = 0
        CustomPlot4x.f2 = 0
    else:
        pass
    if smth.isChecked() == True and smth.text() == "Luca":
        CustomPlot1x.f3 = 1
        CustomPlot2x.f3 = 1
        CustomPlot3x.f3 = 1
        CustomPlot4x.f3 = 1
    elif smth.isChecked() == False and smth.text() == "Luca":
        CustomPlot1x.f3 = 0
        CustomPlot2x.f3 = 0
        CustomPlot3x.f3 = 0
        CustomPlot4x.f3 = 0
    else:
        pass
    if smth.isChecked() == True and smth.text() == "Davide":
        CustomPlot1x.f4 = 1
        CustomPlot2x.f4 = 1
        CustomPlot3x.f4 = 1
        CustomPlot4x.f4 = 1
    elif smth.isChecked() == False and smth.text() == "Davide":
        CustomPlot1x.f4 = 0
        CustomPlot2x.f4 = 0
        CustomPlot3x.f4 = 0
        CustomPlot4x.f4 = 0
    else:
        pass
    if smth.isChecked() == True and smth.text() == "Daniele":
        CustomPlot1x.f5 = 1
        CustomPlot2x.f5 = 1
        CustomPlot3x.f5 = 1
        CustomPlot4x.f5 = 1
    elif smth.isChecked() == False and smth.text() == "Daniele":
        CustomPlot1x.f5 = 0
        CustomPlot2x.f5 = 0
        CustomPlot3x.f5 = 0
        CustomPlot4x.f5 = 0
    else:
        pass
    global retarr
    retarr = [CustomPlot1x.f1, CustomPlot1x.f2, CustomPlot1x.f3, CustomPlot1x.f4, CustomPlot1x.f5, 
              CustomPlot2x.f1, CustomPlot2x.f2, CustomPlot2x.f3, CustomPlot2x.f4, CustomPlot2x.f5, 
              CustomPlot3x.f1, CustomPlot3x.f2, CustomPlot3x.f3, CustomPlot3x.f4, CustomPlot3x.f5, 
              CustomPlot4x.f1, CustomPlot4x.f2, CustomPlot4x.f3, CustomPlot4x.f4, CustomPlot4x.f5]

class Window(QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.initUI() # call the UI set up
    def initUI(self):
        self.setObjectName("Monitoring sensor data")
        self.resize(1500, 768)
        self.layout = QGridLayout(self)
        self.pgcustom1 = CustomPlot1() 
        self.pgcustom2 = CustomPlot2() 
        self.pgcustom3 = CustomPlot3() 
        self.Custom4s = CustomPlot4()
        self.pgcustom4 = pg.plot()
        self.pgcustom4.setTitle("Positions tracking")
        self.pgcustom4.addItem(self.Custom4s)
        self.layout.addWidget(self.pgcustom1,0,0,1,1)
        self.layout.addWidget(self.pgcustom2,0,1,1,1)
        self.layout.addWidget(self.pgcustom3,0,2,1,1)
        self.layout.addWidget(self.pgcustom4,1,1,1,1)
        self.cbx1 = Checkboxes('Roman',self.pgcustom1,self.pgcustom2,self.pgcustom3,self.pgcustom4)
        self.cbx2 = Checkboxes('Matteo',self.pgcustom1,self.pgcustom2,self.pgcustom3,self.pgcustom4)
        self.cbx3 = Checkboxes('Luca',self.pgcustom1,self.pgcustom2,self.pgcustom3,self.pgcustom4)
        self.cbx4 = Checkboxes('Davide',self.pgcustom1,self.pgcustom2,self.pgcustom3,self.pgcustom4)
        self.cbx5 = Checkboxes('Daniele',self.pgcustom1,self.pgcustom2,self.pgcustom3,self.pgcustom4)
        self.layout.addWidget(self.cbx1,2,0,2,1)
        self.layout.addWidget(self.cbx2,4,0,2,1)
        self.layout.addWidget(self.cbx3,6,0,2,1)
        self.layout.addWidget(self.cbx4,8,0,2,1)
        self.layout.addWidget(self.cbx5,10,0,2,1)
        self.show()


def on_message(client, userdata, msg):
    message_real = json.loads(msg.payload.decode())
    
    global iacx,iacy,iacz,iposx,iposy,bufacc,bufposx, bufposy
    for key in bufaccx.keys():
        bufaccx[key][iacx%100] = float(message_real[key]['acc_x'])+random.random()*2.0
        bufaccy[key][iacy%100] = float(message_real[key]['acc_y'])+random.random()*2.0
        bufaccz[key][iacz%100] = float(message_real[key]['acc_z'])+random.random()*2.0
        bufposx[key][iposx%2] = float(message_real[key]['pos_x'])+random.random()*2.0
        bufposy[key][iposy%2] = float(message_real[key]['pos_y'])+random.random()*2.0
    iacx = iacx + 1
    iacy = iacy + 1
    iacz = iacz + 1
    iposx = iposx + 1
    iposy = iposy + 1
        
def on_connect(client,userdata,flags,rc) :
    if rc==0:
        print("client is connected")
        global connected
        connected = True
    else:
        print("connection failed")

client = mqtt_client.Client(client_id, True, None, mqtt_client.MQTTv31)
client.username_pw_set(user,password=password)
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address,port=port)
client.loop_start()

while connected!=True:
    time.sleep(0.2)
    
client.subscribe(topic1)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    Win = Window()
    try:
        while True:
            #time.sleep(1)
            sys.exit(app.exec())
    except KeyboardInterrupt:
        print("exiting")
        client.disconnect()
        client.loop_stop()
