# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PyQtDesignereDOTgq.ui'
##
## Created by: Qt User Interface Compiler version 5.14.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

import sys

from PyQt5.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PyQt5.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.ScrollMods = QScrollArea(self.centralwidget)
        self.ScrollMods.setObjectName(u"ScrollMods")
        self.ScrollMods.setGeometry(QRect(-1, -1, 611, 581))
        self.ScrollMods.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 609, 579))
        self.pushButton = QPushButton(self.scrollAreaWidgetContents)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(260, 210, 75, 21))
        self.ScrollMods.setWidget(self.scrollAreaWidgetContents)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 21))
        self.menuProgramm = QMenu(self.menubar)
        self.menuProgramm.setObjectName(u"menuProgramm")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuProgramm.menuAction())

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.menuProgramm.setTitle(QCoreApplication.translate("MainWindow", u"Programm", None))
    # retranslateUi

def main():
    app = QApplication(sys.argv)
    ex = Ui_MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
