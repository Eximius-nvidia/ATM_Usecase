# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ATM_Dashboard_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DashboardWindow(object):
    def setupUi(self, DashboardWindow):
        DashboardWindow.setObjectName("DashboardWindow")
        DashboardWindow.resize(1340, 760)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DashboardWindow.sizePolicy().hasHeightForWidth())
        DashboardWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(DashboardWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.label_Title = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.label_Title.setFont(font)
        self.label_Title.setAutoFillBackground(True)
        self.label_Title.setTextFormat(QtCore.Qt.RichText)
        self.label_Title.setScaledContents(True)
        self.label_Title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_Title.setWordWrap(False)
        self.label_Title.setObjectName("label_Title")
        self.gridLayout.addWidget(self.label_Title, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout.addWidget(self.label_6)
        self.lcdNumber_Online = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber_Online.setFrameShape(QtWidgets.QFrame.Box)
        self.lcdNumber_Online.setFrameShadow(QtWidgets.QFrame.Raised)
        self.lcdNumber_Online.setSmallDecimalPoint(True)
        self.lcdNumber_Online.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcdNumber_Online.setObjectName("lcdNumber_Online")
        self.horizontalLayout.addWidget(self.lcdNumber_Online)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout.addWidget(self.label_5)
        self.lcdNumber_Offline = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber_Offline.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcdNumber_Offline.setObjectName("lcdNumber_Offline")
        self.horizontalLayout.addWidget(self.lcdNumber_Offline)
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout.addWidget(self.label_7)
        self.lcdNumber_Total = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber_Total.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcdNumber_Total.setObjectName("lcdNumber_Total")
        self.horizontalLayout.addWidget(self.lcdNumber_Total)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setLineWidth(2)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.gridLayout.addWidget(self.tableWidget, 2, 0, 1, 1)
        DashboardWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(DashboardWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1340, 21))
        self.menubar.setObjectName("menubar")
        DashboardWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(DashboardWindow)
        self.statusbar.setObjectName("statusbar")
        DashboardWindow.setStatusBar(self.statusbar)

        self.retranslateUi(DashboardWindow)
        QtCore.QMetaObject.connectSlotsByName(DashboardWindow)

    def retranslateUi(self, DashboardWindow):
        _translate = QtCore.QCoreApplication.translate
        DashboardWindow.setWindowTitle(_translate("DashboardWindow", "ATM Dashboard"))
        self.label_Title.setText(_translate("DashboardWindow", "ATM Centers Online Dashboard"))
        self.label_6.setText(_translate("DashboardWindow", "ATMs Online"))
        self.label_5.setText(_translate("DashboardWindow", "ATMs Offline"))
        self.label_7.setText(_translate("DashboardWindow", "ATMs Total"))
        self.tableWidget.setSortingEnabled(False)