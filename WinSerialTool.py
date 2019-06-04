# -*- coding: utf-8 -*-
import sys
import PublicLib.public as pub
from PyQt5 import QtWidgets
from MainWindow import MainWindow

__author__ = 'jerry'


if __name__ == '__main__':
    pub.loggingConfig('logging.conf')
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

