# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'GUI_BMS.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(874, 856)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.title_label = QLabel(self.centralwidget)
        self.title_label.setObjectName(u"title_label")
        self.title_label.setGeometry(QRect(10, 20, 781, 31))
        font = QFont()
        font.setFamily(u"Verdana")
        font.setPointSize(20)
        self.title_label.setFont(font)
        self.title_label.setFrameShape(QFrame.Box)
        self.title_label.setFrameShadow(QFrame.Sunken)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.plugin_input_button = QPushButton(self.centralwidget)
        self.plugin_input_button.setObjectName(u"plugin_input_button")
        self.plugin_input_button.setGeometry(QRect(30, 100, 731, 31))
        font1 = QFont()
        font1.setFamily(u"Verdana")
        font1.setPointSize(12)
        self.plugin_input_button.setFont(font1)
        self.plugin_input_label = QLabel(self.centralwidget)
        self.plugin_input_label.setObjectName(u"plugin_input_label")
        self.plugin_input_label.setGeometry(QRect(230, 70, 331, 20))
        self.plugin_input_label.setFont(font1)
        self.plugin_input_label.setAlignment(Qt.AlignCenter)
        self.object_input_label = QLabel(self.centralwidget)
        self.object_input_label.setObjectName(u"object_input_label")
        self.object_input_label.setGeometry(QRect(230, 140, 331, 20))
        self.object_input_label.setFont(font1)
        self.object_input_label.setAlignment(Qt.AlignCenter)
        self.object_input_button = QPushButton(self.centralwidget)
        self.object_input_button.setObjectName(u"object_input_button")
        self.object_input_button.setGeometry(QRect(30, 170, 731, 31))
        self.object_input_button.setFont(font1)
        self.polygons_label = QLabel(self.centralwidget)
        self.polygons_label.setObjectName(u"polygons_label")
        self.polygons_label.setGeometry(QRect(150, 220, 531, 20))
        self.polygons_label.setFont(font1)
        self.polygons_label.setAlignment(Qt.AlignCenter)
        self.polygons_lineEdit = QLineEdit(self.centralwidget)
        self.polygons_lineEdit.setObjectName(u"polygons_lineEdit")
        self.polygons_lineEdit.setGeometry(QRect(30, 260, 731, 31))
        font2 = QFont()
        font2.setFamily(u"Verdana")
        font2.setPointSize(10)
        font2.setItalic(True)
        self.polygons_lineEdit.setFont(font2)
        self.polygons_lineEdit.setAlignment(Qt.AlignCenter)
        self.diffres_label = QLabel(self.centralwidget)
        self.diffres_label.setObjectName(u"diffres_label")
        self.diffres_label.setGeometry(QRect(140, 320, 531, 20))
        self.diffres_label.setFont(font1)
        self.diffres_label.setAlignment(Qt.AlignCenter)
        self.normres_label = QLabel(self.centralwidget)
        self.normres_label.setObjectName(u"normres_label")
        self.normres_label.setGeometry(QRect(140, 420, 531, 20))
        self.normres_label.setFont(font1)
        self.normres_label.setAlignment(Qt.AlignCenter)
        self.decimate_button = QPushButton(self.centralwidget)
        self.decimate_button.setObjectName(u"decimate_button")
        self.decimate_button.setGeometry(QRect(30, 550, 721, 31))
        font3 = QFont()
        font3.setFamily(u"Verdana")
        font3.setPointSize(12)
        font3.setBold(True)
        font3.setWeight(75)
        self.decimate_button.setFont(font3)
        self.decimate_button.setAutoFillBackground(False)
        self.diffres_comboBox = QComboBox(self.centralwidget)
        self.diffres_comboBox.addItem("")
        self.diffres_comboBox.addItem("")
        self.diffres_comboBox.addItem("")
        self.diffres_comboBox.addItem("")
        self.diffres_comboBox.addItem("")
        self.diffres_comboBox.addItem("")
        self.diffres_comboBox.setObjectName(u"diffres_comboBox")
        self.diffres_comboBox.setGeometry(QRect(30, 350, 721, 31))
        self.diffres_comboBox.setFont(font2)
        self.normres_comboBox = QComboBox(self.centralwidget)
        self.normres_comboBox.addItem("")
        self.normres_comboBox.addItem("")
        self.normres_comboBox.addItem("")
        self.normres_comboBox.addItem("")
        self.normres_comboBox.addItem("")
        self.normres_comboBox.addItem("")
        self.normres_comboBox.setObjectName(u"normres_comboBox")
        self.normres_comboBox.setGeometry(QRect(30, 450, 721, 31))
        self.normres_comboBox.setFont(font2)
        self.normres_comboBox.setLayoutDirection(Qt.LeftToRight)
        self.plainTextEdit = QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        self.plainTextEdit.setGeometry(QRect(30, 630, 721, 101))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 874, 21))
        self.menuAutomatic_Bakemyscan = QMenu(self.menubar)
        self.menuAutomatic_Bakemyscan.setObjectName(u"menuAutomatic_Bakemyscan")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuAutomatic_Bakemyscan.menuAction())

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.title_label.setText(QCoreApplication.translate("MainWindow", u"AUTOMATIC BAKE MY SCAN", None))
        self.plugin_input_button.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.plugin_input_label.setText(QCoreApplication.translate("MainWindow", u"Get the plugin global folder below", None))
        self.object_input_label.setText(QCoreApplication.translate("MainWindow", u"Get the object file below", None))
        self.object_input_button.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.polygons_label.setText(QCoreApplication.translate("MainWindow", u"How many polygons do you want for the resulting object?", None))
        self.polygons_lineEdit.setText(QCoreApplication.translate("MainWindow", u"Enter whole number (no decimals)", None))
        self.diffres_label.setText(QCoreApplication.translate("MainWindow", u"What resolution should the diffuse texture be?", None))
        self.normres_label.setText(QCoreApplication.translate("MainWindow", u"What resolution should the normal texture be?", None))
        self.decimate_button.setText(QCoreApplication.translate("MainWindow", u"Decimate", None))
        self.diffres_comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Choose the resolution", None))
        self.diffres_comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"256", None))
        self.diffres_comboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"512", None))
        self.diffres_comboBox.setItemText(3, QCoreApplication.translate("MainWindow", u"1024", None))
        self.diffres_comboBox.setItemText(4, QCoreApplication.translate("MainWindow", u"2048", None))
        self.diffres_comboBox.setItemText(5, QCoreApplication.translate("MainWindow", u"4096", None))

        self.normres_comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Choose the resolution", None))
        self.normres_comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"256", None))
        self.normres_comboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"512", None))
        self.normres_comboBox.setItemText(3, QCoreApplication.translate("MainWindow", u"1024", None))
        self.normres_comboBox.setItemText(4, QCoreApplication.translate("MainWindow", u"2048", None))
        self.normres_comboBox.setItemText(5, QCoreApplication.translate("MainWindow", u"4096", None))

        self.normres_comboBox.setCurrentText(QCoreApplication.translate("MainWindow", u"Choose the resolution", None))
        self.menuAutomatic_Bakemyscan.setTitle(QCoreApplication.translate("MainWindow", u"Automatic Bakemyscan", None))
    # retranslateUi

