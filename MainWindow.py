from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from MainWnd_UiHandler import MainWnd_UiHandler
from SerialDlg_UiHandler import SerialDlg_UiHandler
import logging
import json
from OpenExcelTestPlan import ExcelPlan
from DownLink import DownLinkThread
import threading
import queue
# from Protocol.protocol import prtlthread

logger = logging.getLogger('main.MainWindow')


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self)

        self.qRecv = queue.Queue()
        self.qSocRecv = None
        logger.info('Main Window logger start')
        self.uim = MainWnd_UiHandler(self.qRecv)
        self.uid = SerialDlg_UiHandler()
        self.uim.setupUi(self)
        self.createActions()
        self.test = {"State":"stop", "Num":0, "Index":0, "timeout":0,
                     "SendFrame":None, "Answer":None}

        self.uim.startTestButton.setEnabled(False)

        config = self.loadTestPlanDefaultSettings()
        logger.info(config)
        self.uim.planComboBox.clear()
        planList = []
        for i in range(config['planNum']):
            print(config['plan' + str(i + 1)])
            planList += [config['plan' + str(i + 1)]]
        self.uim.planComboBox.addItems(planList)

    def loggingConfig(self):
        logging.config.fileConfig('logging.conf')
        root_logger = logging.getLogger('root')
        root_logger.debug('Logging System Start')

        logger = logging.getLogger('main')
        logger.info('Logging main Start')

    def loadTestPlanDefaultSettings(self):
        try:
            planConfigFile = open("configplan.json")
            defaultPlanConfig = json.load(planConfigFile)
            print(defaultPlanConfig)
        finally:
            if planConfigFile:
                planConfigFile.close()
                return defaultPlanConfig

    def loadSerialDefaultSettings(self):
        try:
            configFile = open("config.json")
            defaultConfig = json.load(configFile)
            print(defaultConfig)
        finally:
            if configFile:
                configFile.close()
                return defaultConfig

    def closeDlgReEvent(self):
        # self.uid.dia.hide()  # 隐藏此窗口
        # self.mainWindow = Ui_MainWindow()
        # self.uim.show()  # 显示登录窗口
        logger.info('SerialDlgWindow closeEvent')

    def closeDlgAcEvent(self):
        port = self.uid.dia.cbbPortName.currentText()
        baud = int(self.uid.dia.cbbBaudRate.currentText())
        parity = self.uid.dia.cbbParity.currentText()
        config = {'port': port, 'baud': baud, "parity": parity}
        configFile = json.dumps(config)
        try:
            f = open("config.json", 'w')
            f.write(configFile)
        finally:
            f.close()
        # plan = self.uim.planComboBox.currentText()
        # prtlthread(self, plan)
        DownLinkThread(self=self)

    def closeEvent(self, e):
        """
        This will called when user close the window. save the configurations here.
        :param e:
        :return: Nothing
        TODO: Can this be placed in a better place?
        """
        reply = QtWidgets.QMessageBox.question(self, '警告', '退出后测试将停止,\n你确认要退出吗？', \
                                               QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            if self.uid.flags["__isopen__"] is True:
                self.uid.flags = {"__isopen__": False, "__datatype__": "ascii"}
                self.uid.serial.terminate(False)
                self.uid.serial.close()
            e.accept()
        else:
            e.ignore()

    def createActions(self):
        # 串口设置窗口事件
        self.uid.dia.buttonBox.accepted.connect(self.closeDlgAcEvent)
        self.uid.dia.buttonBox.rejected.connect(self.closeDlgReEvent)
        self.uid.serial.received.connect(self.uim.onRecvData)
        # self.uid.dia.OpenSerialButton.clicked.connect(self._btnSerialOpenEvent)
        # self.uid.dia.CloseSerialButton.clicked.connect(self._btnSerialCloseEvent)

        # 主窗口事件
        self.uim.BaseInfoButton.clicked.connect(self._btnSetEvent)
        self.uim.planButton.clicked.connect(self._btnTestPlanEvent)
        self.uim.startTestButton.clicked.connect(self._btnStartTest)

    # 串口设置功能
    def _btnSetEvent(self):
        ports = self.uid.serial.searchSerialPort()
        self.uid.dia.cbbPortName.clear()
        self.uid.dia.cbbPortName.addItems(ports)
        config = self.loadSerialDefaultSettings()
        if ports.__contains__(config['port']):
            self.uid.dia.cbbPortName.setCurrentText(config['port'])
        self.uid.dia.cbbBaudRate.setCurrentText(str(config['baud']))
        self.uid.dia.cbbParity.setCurrentText(config['parity'])
        self.uid.show()

    # 测试方案载入
    def _btnTestPlanEvent(self):
        planText = self.uim.planComboBox.currentText()
        logger.info(planText)
        self.uim.PlanTextEdit.clear()
        self.plan = ExcelPlan(planText)
        if self.plan.row_count == 0:
            print(planText+" is not exist!")
            logger.info('ExcelPlan ' +planText+" is not exist!")
            return

        showinfo = planText
        num = self.plan.Num()
        self.test["Num"] = num

        self.uim.AnaTableWidget.setColumnCount(6)  # 0：名称，1：命令，2：DI，3：下行数据，4：上行数据，5：结果
        self.uim.AnaTableWidget.setRowCount(num)
        self.uim.AnaTableWidget.setColumnWidth(0, 280)  # 设置j列的宽度

        for i in range(0, num):
            showinfo += self.plan.Name(i) + ':\n' + self.plan.Data(i) + '\n\n'
            self.uim.AnaTableWidget.setItem(i, 0, QTableWidgetItem(self.plan.Name(i)))
            self.uim.AnaTableWidget.setItem(i, 1, QTableWidgetItem(self.plan.Cmd(i)))
            self.uim.AnaTableWidget.setItem(i, 2, QTableWidgetItem(self.plan.Data(i)))
            self.uim.AnaTableWidget.setItem(i, 3, QTableWidgetItem(self.plan.Value(i)))
        self.uim.PlanTextEdit.append(showinfo)
        self.test["State"] = "stop"
        self.uim.startTestButton.setEnabled(True)


    def _btnStartTest(self):
        text = self.uim.startTestButton.text()
        if text == "测试结束(串口)":
            self.uim.startTestButton.setText("开始测试(串口)")
        elif text == "开始测试(串口)":
            self.test["State"] = "start"
            self.uim.startTestButton.setText("测试中(串口)")
        elif text == "测试中(串口)":
            self.test["State"] = "stop"
            self.uim.startTestButton.setText("测试结束(串口)")
        return