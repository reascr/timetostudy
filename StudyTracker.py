#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'StudyTracker.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
#

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, QTime, Qt
import sys
import time
from datetime import datetime, date
import csv
import os
import pandas as pd
import matplotlib.pyplot as plt 
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


# directory of script
script_dir = os.path.dirname(os.path.realpath(__file__))

# 
today = date.today()
current_date = today.strftime("%d.%m.%Y")


DEFAULT_BUTTON_STYLE = "background-color: rgba(241, 204, 255, 194); color: grey; border-style: outset; border-width: 5px;  border-radius: 15px; border-color: rgb(224, 238, 245); padding: 10px"

rows = []
with open(os.path.join(script_dir, "Data.csv"), encoding = 'utf-8') as e:
    reader = csv.reader(e)
    for row in reader:
        rows.append(row)
    last_checktime = float(rows[-1][1]) * 3600
    last_checktime_updated = time.strftime('%H:%M:%S', time.gmtime(int(last_checktime)))
    h, m, s = last_checktime_updated.split(":")
    # Durchschnittliche Zeit pro Tag
    all_time = 0
    for row in rows:
        all_time = all_time + float(row[1])

    mean_time = (all_time/ len(rows)) * 3600
    up_mean_time = time.strftime('%H:%M:%S', time.gmtime(int(mean_time)))
    if current_date != rows[-1][0]:
        h, m, s = 0,0,0
     

class Ui_MainWindow(object):
    TIMER_OBJECT = None 
    STARTED = False
    timee = QtCore.QTime(int(h), int(m), int(s))

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        # prevent MainWindow from resizing
        MainWindow.setFixedSize(900, 720)
        #MainWindow.resize(1440, 786)
        MainWindow.setStyleSheet("background-color: rgba(190, 230, 220, 107)")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Current Time Label
        font = QtGui.QFont()
        font.setPointSize(20)

        self.label0 = QtWidgets.QLabel(self.centralwidget)
        self.label0.setGeometry(QtCore.QRect(130, 80, 211, 131))
        self.label0.setFont(font)
        self.label0.setStyleSheet("color:grey")

        # create a timer object
        timer = QTimer(MainWindow)

        # adding action to timer
        timer.timeout.connect(self.showTime)


        # update timer every second
        timer.start(1000)

        font = QtGui.QFont()
        font.setPointSize(40)

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(360, 260, 221, 201))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(os.path.join(script_dir, "Icon.png")))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")

        # Label für Timetracker
        self.label2 = QtWidgets.QLabel(self.centralwidget)
        self.label2.setGeometry(QtCore.QRect(650, 300, 221, 131))
        self.label2.setText("TIME")
        self.label2.setFont(font)
        self.label2.setStyleSheet("color:grey")
        
        font.setPointSize(20)

        # Label für Durchschnittszeit
        self.label3 = QtWidgets.QLabel(self.centralwidget)
        self.label3.setGeometry(QtCore.QRect(620, 80, 221, 131))
        self.label3.setText("Average Productivity: \n" + str(up_mean_time))
        self.label3.setFont(font)
        self.label3.setStyleSheet("color:grey")
        

        
        # Canvas für die Plots
        self.figure = plt.figure()
    
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setFixedSize(400,400)

        font = QtGui.QFont("Didot", QtGui.QFont.Bold)
        font.setPointSize(23)

        self.b0 = QtWidgets.QPushButton(self.centralwidget)
        self.b0.clicked.connect(self.plot)
        self.b0.setGeometry(QtCore.QRect(80, 300, 211, 131))
        self.b0.setStyleSheet("background-color: rgb(200, 255, 226); color: grey; border-style: outset; border-width: 5px;  border-radius: 15px; border-color: rgb(213, 255, 213); padding: 10px")
        self.b0.setFont(font)

        font = QtGui.QFont("Didot", QtGui.QFont.Bold)
        font.setPointSize(30)

        self.b1 = QtWidgets.QPushButton(self.centralwidget)
        self.b1.setGeometry(QtCore.QRect(360, 80, 221, 131))
        self.b1.setFont(font)
        self.b1.setStyleSheet(DEFAULT_BUTTON_STYLE)
        self.b1.setObjectName("b1")
        self.b1.clicked.connect(self.clickedb1)

        self.b2 = QtWidgets.QPushButton(self.centralwidget)
        self.b2.setGeometry(QtCore.QRect(360, 520, 221, 131))
        self.b2.setFont(font)
        self.b2.setStyleSheet(DEFAULT_BUTTON_STYLE)
        self.b2.setObjectName("b2")
        self.b2.clicked.connect(self.clickedb2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1440, 29))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.menubar.setFont(font)
        self.menubar.setObjectName("menubar")
        self.menuStatistiken = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.menuStatistiken.setFont(font)
        self.menuStatistiken.setObjectName("menuStatistiken")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionGehe_zu_Statistiken = QtWidgets.QAction(MainWindow)
        self.actionGehe_zu_Statistiken.setObjectName("actionGehe_zu_Statistiken")
        self.menuStatistiken.addAction(self.actionGehe_zu_Statistiken)
        self.menubar.addAction(self.menuStatistiken.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Study Tracker"))
        self.b0.setText(_translate("MainWindow", "Wochenübersicht"))
        self.b1.setText(_translate("MainWindow", "Start"))
        self.b2.setText(_translate("MainWindow", "Pause"))
        self.menuStatistiken.setTitle(_translate("MainWindow", "Statistiken"))
        self.actionGehe_zu_Statistiken.setText(_translate("MainWindow", "Gehe zu Statistiken"))
    
    
    # method called by timer

    def showTime(self):
        current_time = QTime.currentTime()
        label0_time = current_time.toString("hh:mm:ss")
        self.label0.setText("current time: \n " + label0_time)
        if Ui_MainWindow.STARTED:
            Ui_MainWindow.timee = Ui_MainWindow.timee.addSecs(1)
            label_time = Ui_MainWindow.timee.toString("hh:mm:ss")
            self.label2.setText(label_time)
        else: 
            self.label2.setText(Ui_MainWindow.timee.toString("hh:mm:ss"))

        
     # plot function
    def plot(self):
        self.df = pd.read_csv('/Users/rea/Documents/TimeTrackerApp/Data.csv', header=None)
        self.df.columns = ['Datum', 'Zeit (h)'] 
        self.figure.clear()
        self.df.plot(kind='bar', x='Datum', y='Zeit (h)')
        plt.tight_layout()
        plt.show()
        self.canvas.draw()

    def clickedb1(self):
        Ui_MainWindow.STARTED = True
        self.b1.setStyleSheet("background-color: rgb(208, 182, 228); color: grey; border-style: inset; border-width: 2px;  border-radius: 10px; border-color: beige; padding: 10px")
        self.b2.setStyleSheet(DEFAULT_BUTTON_STYLE)
        rows = []
        # was wenn Datei noch nicht existiert?
        try:
            with open(os.path.join(script_dir, "Data.csv"), encoding = 'utf-8') as e:
                reader = csv.reader(e)
                for row in reader:
                    rows.append(row)
                if rows[-1][0] == current_date:
                    last_checktime = float(rows[-1][1]) * 3600
                    last_checktime_updated = time.strftime('%H:%M:%S', time.gmtime(int(last_checktime)))
                    self.label2.setText(str(last_checktime_updated))
                else: 
                    self.label2.setText("00:00:00")
        except:
            self.label2.setText("00:00:00")
        Ui_MainWindow.TIMER_OBJECT = time.time()
        

        
    def clickedb2(self):
        Ui_MainWindow.STARTED = False
        self.b1.setStyleSheet(DEFAULT_BUTTON_STYLE)
        self.b2.setStyleSheet("background-color: rgb(208, 182, 228); color: grey; border-style: inset; border-width: 2px;  border-radius: 10px; border-color: beige; padding: 10px")
        end = time.time()
        updated_date = date.today()
        updated_date_form = updated_date.strftime("%d.%m.%Y")
        updated_time = datetime.now()
        updated_time_form = updated_time.strftime("%H:%M:%S")
        hours = (end-Ui_MainWindow.TIMER_OBJECT)/3600
        

        DateTime = [current_date, hours]

# Store data as csv
        rows = []
        try:
            # with open('/Users/rea/Documents/TimeTrackerApp/Data.csv', encoding ='utf-8') as e:
            with open(os.path.join(script_dir, "Data.csv"), encoding = 'utf-8') as e:
                reader = csv.reader(e)
                for row in reader:
                    rows.append(row)
                    

                if rows[-1][0] == DateTime[0]:
                    # addierte Zeit für current date
                    newtime = float(rows[-1][1]) + hours

                    # letzten Zeileneintrag löschen
                    rows.pop()
                    rows.append([current_date, newtime])
                        
                    # csv-Datei clearen
                    olddatafile = open(os.path.join(script_dir, "Data.csv"), 'w')
                    olddatafile.truncate()
                    olddatafile.close()

                    # csv-Datei neu beschreiben, mit allen Zeilen 

                    with open(os.path.join(script_dir, "Data.csv"), 'a', encoding='utf-8') as f:
                        writer = csv.writer(f)

                        for row in rows:
                            writer.writerow(row)
                else:
                    with open(os.path.join(script_dir, "Data.csv"), 'a', encoding='utf-8') as f:
                        writer = csv.writer(f)
                        writer.writerow(DateTime)

                            

        except:
            with open(os.path.join(script_dir, "Data.csv"), 'a', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(DateTime)

        with open(os.path.join(script_dir, "Data.csv"), encoding = 'utf-8') as e:
            reader = csv.reader(e)
            for row in reader:
                rows.append(row)
            last_checktime = float(rows[-1][1]) * 3600
            last_checktime_updated = time.strftime('%H:%M:%S', time.gmtime(int(last_checktime)))
            h, m, s = last_checktime_updated.split(":")
            # Durchschnittliche Zeit pro Tag
            all_time = 0
            for row in rows:
                all_time = all_time + float(row[1])

            mean_time = (all_time/ len(rows)) * 3600
            up_mean_time = time.strftime('%H:%M:%S', time.gmtime(int(mean_time)))
            self.label3.setText("Average Productivity: \n" + str(up_mean_time))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
