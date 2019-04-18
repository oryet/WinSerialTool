
from PyQt5.QtGui import QTextCursor
from StSerial import StSerial
import serial
from PyQt5 import QtGui, QtCore, QtWidgets
from serialsetDialog import Ui_Dialog
import logging
import json

logger = logging.getLogger('main.MainWindow')


class SerialDlg_UiHandler(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self)

        logger.info('Dialog Window logger start')
        self.dia = Ui_Dialog()
        self.flags = {"__isopen__": False, "__datatype__": "ascii"}
        self.dia.setupUi(self)
        self.serial = StSerial()
        self.dia.OpenSerialButton.clicked.connect(self.__onOpenPort)
        self.dia.CloseSerialButton.clicked.connect(self.__closePort)
        self.dia.CloseSerialButton.setEnabled(False)
        self.dia_log = ""

    def getPortSettings(self):
        """
        This method will read out all serial setting in UI
        :return: settings of the serial.
        """
        settings = {"port": self.dia.cbbPortName.currentText(), "baud": self.dia.cbbBaudRate.currentText(),
                    "bytesize": int(self.dia.cbbDataBit.currentText()), "parity": self.dia.cbbParity.currentText()[:1],
                    "stopbits": int(self.dia.cbbStopBit.currentText()), "timeout": 1}

        # For pySerial, parity input shoud be
        # PARITY_NONE, PARITY_EVEN, PARITY_ODD, PARITY_MARK, PARITY_SPACE = 'N', 'E', 'O', 'M', 'S'
        logger.info(settings)
        return settings

    def __onOpenPort(self, settings=None):
        if self.flags["__isopen__"] is False:
            if not settings:
                settings = self.getPortSettings()
            self.serial.terminate(True)
            self.serial.open(settings)
            self.serial.start()
            self.flags = {"__isopen__": True, "__datatype__": "ascii"}
            self.dia.OpenSerialButton.setEnabled(False)
            self.dia.CloseSerialButton.setEnabled(True)
            logger.info('SerialDlgWindow __onOpenPort OK')

    '''
    def __onSendData(self):
        logger.info("Send Data Clicked")
        #        data, type = self.ui.getDataAndType()
        #        self.ui.onSendData(data, type)
        #        dataArray = Utils.getByteArray(data,type)
        dataArray = self.ui.onSendData(None)
        logger.info(dataArray)
        self.serial.send(dataArray)


    def __openPort(self, settings):
        StSerial.open(settings)
    '''
    def __closePort(self):
        if self.flags["__isopen__"] is True:
            self.flags = {"__isopen__": False, "__datatype__": "ascii"}
            self.serial.terminate(False)
            self.serial.close()
            self.dia.OpenSerialButton.setEnabled(True)
            self.dia.CloseSerialButton.setEnabled(False)
            logger.info('SerialDlgWindow __closePort OK')
    '''
    def clearRxText(self):
        self.ui.pteRx.clear()
    '''

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    mainWindow = SerialDlg_UiHandler()

    ports = mainWindow.serial.searchSerialPort()
    mainWindow.dia.cbbPortName.clear()
    mainWindow.dia.cbbPortName.addItems(ports)

    mainWindow.show()
    sys.exit(app.exec_())