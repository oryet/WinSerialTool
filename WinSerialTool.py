# -*- coding: utf-8 -*-
import json
import logging
import logging.config
import sys

from PyQt5 import QtWidgets

# from StSerial import StSerial
from MainWindow import MainWindow

__author__ = 'jerry'


def loggingConfig():
    logging.config.fileConfig('logging.conf')
    root_logger = logging.getLogger('root')
    root_logger.debug('Logging System Start')
    logger = logging.getLogger('main')
    logger.info('Logging main Start')


# def loadDefaultSettings():
#     try:
#         configFile = open("config.json")
#         defaultConfig = json.load(configFile)
#         print(defaultConfig)
#     finally:
#         if configFile:
#             configFile.close()
#             return defaultConfig


if __name__ == '__main__':
    loggingConfig()
    # ports = StSerial.searchSerialPort()
    # print(ports)

    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    # mainWindow.ui.cbbPortName.addItems(ports)
    # config = loadDefaultSettings()
    # if ports.__contains__(config['port']):
    #     mainWindow.ui.cbbPortName.setCurrentText(config['port'])
    # mainWindow.ui.cbbBaudRate.setCurrentText(str(config['baud']))
    # mainWindow.ui.cbRxHex.setChecked(config['rxHex'])
    # mainWindow.ui.cbRxAscii.setChecked(config['rxASCII'])
    # mainWindow.ui.cbNewLine.setChecked(config['txNewLine'])
    mainWindow.show()
    sys.exit(app.exec_())

