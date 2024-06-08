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

        # Title Label
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

        # Plugin Input Label and Button
        font1 = QFont()
        font1.setFamily(u"Verdana")
        font1.setPointSize(12)
        
        self.plugin_input_label = QLabel(self.centralwidget)
        self.plugin_input_label.setObjectName(u"plugin_input_label")
        self.plugin_input_label.setGeometry(QRect(230, 70, 331, 20))
        self.plugin_input_label.setFont(font1)
        self.plugin_input_label.setAlignment(Qt.AlignCenter)

        self.plugin_input_button = QPushButton(self.centralwidget)
        self.plugin_input_button.setObjectName(u"plugin_input_button")
        self.plugin_input_button.setGeometry(QRect(30, 100, 731, 31))
        self.plugin_input_button.setFont(font1)

        # Blender Input Label and Button
        self.blender_input_label = QLabel(self.centralwidget)
        self.blender_input_label.setObjectName(u"blender_input_label")
        self.blender_input_label.setGeometry(QRect(230, 140, 331, 20))
        self.blender_input_label.setFont(font1)
        self.blender_input_label.setAlignment(Qt.AlignCenter)
        
        self.blender_input_button = QPushButton(self.centralwidget)
        self.blender_input_button.setObjectName(u"blender_input_button")
        self.blender_input_button.setGeometry(QRect(30, 170, 731, 31))
        self.blender_input_button.setFont(font1)
        
        # Object Input Label and Button
        self.object_input_label = QLabel(self.centralwidget)
        self.object_input_label.setObjectName(u"object_input_label")
        self.object_input_label.setGeometry(QRect(230, 210, 331, 20))
        self.object_input_label.setFont(font1)
        self.object_input_label.setAlignment(Qt.AlignCenter)

        self.object_input_button = QPushButton(self.centralwidget)
        self.object_input_button.setObjectName(u"object_input_button")
        self.object_input_button.setGeometry(QRect(30, 240, 731, 31))
        self.object_input_button.setFont(font1)

        # Polygons Label and LineEdit
        font2 = QFont()
        font2.setFamily(u"Verdana")
        font2.setPointSize(10)
        font2.setItalic(True)

        self.polygons_label = QLabel(self.centralwidget)
        self.polygons_label.setObjectName(u"polygons_label")
        self.polygons_label.setGeometry(QRect(150, 290, 531, 20))
        self.polygons_label.setFont(font1)
        self.polygons_label.setAlignment(Qt.AlignCenter)

        self.polygons_lineEdit = QLineEdit(self.centralwidget)
        self.polygons_lineEdit.setObjectName(u"polygons_lineEdit")
        self.polygons_lineEdit.setGeometry(QRect(30, 320, 731, 31))
        self.polygons_lineEdit.setFont(font2)
        self.polygons_lineEdit.setAlignment(Qt.AlignCenter)

        # Diffuse Resolution Label and ComboBox
        self.diffres_label = QLabel(self.centralwidget)
        self.diffres_label.setObjectName(u"diffres_label")
        self.diffres_label.setGeometry(QRect(140, 370, 531, 20))
        self.diffres_label.setFont(font1)
        self.diffres_label.setAlignment(Qt.AlignCenter)

        self.diffres_comboBox = QComboBox(self.centralwidget)
        self.diffres_comboBox.addItem("")
        self.diffres_comboBox.addItem("")
        self.diffres_comboBox.addItem("")
        self.diffres_comboBox.addItem("")
        self.diffres_comboBox.addItem("")
        self.diffres_comboBox.addItem("")
        self.diffres_comboBox.setObjectName(u"diffres_comboBox")
        self.diffres_comboBox.setGeometry(QRect(30, 400, 721, 31))
        self.diffres_comboBox.setFont(font2)

        # Normal Resolution Label and ComboBox
        self.normres_label = QLabel(self.centralwidget)
        self.normres_label.setObjectName(u"normres_label")
        self.normres_label.setGeometry(QRect(140, 450, 531, 20))
        self.normres_label.setFont(font1)
        self.normres_label.setAlignment(Qt.AlignCenter)

        self.normres_comboBox = QComboBox(self.centralwidget)
        self.normres_comboBox.addItem("")
        self.normres_comboBox.addItem("")
        self.normres_comboBox.addItem("")
        self.normres_comboBox.addItem("")
        self.normres_comboBox.addItem("")
        self.normres_comboBox.addItem("")
        self.normres_comboBox.setObjectName(u"normres_comboBox")
        self.normres_comboBox.setGeometry(QRect(30, 480, 721, 31))
        self.normres_comboBox.setFont(font2)
        self.normres_comboBox.setLayoutDirection(Qt.LeftToRight)

        # Decimate Button
        font3 = QFont()
        font3.setFamily(u"Verdana")
        font3.setPointSize(12)
        font3.setBold(True)
        font3.setWeight(75)

        self.decimate_button = QPushButton(self.centralwidget)
        self.decimate_button.setObjectName(u"decimate_button")
        self.decimate_button.setGeometry(QRect(30, 550, 721, 31))
        self.decimate_button.setFont(font3)
        self.decimate_button.setAutoFillBackground(False)

        # Console Output Area
        self.console = QPlainTextEdit(self.centralwidget)
        self.console.setObjectName(u"console")
        self.console.setGeometry(QRect(30, 590, 731, 200))
        self.console.setFont(font2)
        self.console.setReadOnly(True)

        # Set Central Widget
        MainWindow.setCentralWidget(self.centralwidget)

        # Menubar
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 874, 21))
        self.menuAutomatic_Bakemyscan = QMenu(self.menubar)
        self.menuAutomatic_Bakemyscan.setObjectName(u"menuAutomatic_Bakemyscan")
        MainWindow.setMenuBar(self.menubar)

        # Statusbar
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # Add Menu Action
        self.menubar.addAction(self.menuAutomatic_Bakemyscan.menuAction())

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.title_label.setText(QCoreApplication.translate("MainWindow", u"AUTOMATIC BAKE MY SCAN", None))
        self.plugin_input_button.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.plugin_input_label.setText(QCoreApplication.translate("MainWindow", u"Get the plugin global folder below", None))
        self.object_input_label.setText(QCoreApplication.translate("MainWindow", u"Get the object file below", None))
        self.object_input_button.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.blender_input_label.setText(QCoreApplication.translate("MainWindow", u"Get your Blender executable", None))
        self.blender_input_button.setText(QCoreApplication.translate("MainWindow", u"...", None))
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
        self.menuAutomatic_Bakemyscan.setTitle(QCoreApplication.translate("MainWindow", u"Automatic Bakemyscan", None))
