# -*- coding: utf-8 -*-
from pytesttoolMainWindow import Ui_MainWindow as dreamSerial_MainWindow

class MainWnd_UiHandler(dreamSerial_MainWindow):
    def __init__(self, q):
        dreamSerial_MainWindow.__init__(self)
        self.q = q

    def getDataAndType(self):
        return self.leTx.text(), self.cbbTxType.currentText().lower()

    def onSendData(self, data=None, _type="hex"):
        if not data:
            data = self.leTx.text()
        if _type == "hex":
            data = [int(x, 16) for x in data.replace('0x', '').split()]
        else:
            data = bytes(data, 'utf-8')

        return data

    def onRecvData(self, data):
        if len(data) < 5:
            return
        self.q.put(data)