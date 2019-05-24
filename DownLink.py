# coding:utf-8
import threading
import showinfo
import time
from PublicLib.Protocol.protocol import prtl2Make
from PublicLib.Protocol.protocol import judgePrtl
from PublicLib.Protocol.protocol import prtlDealFrame
from PyQt5.QtWidgets import QTableWidgetItem
import pandas as pd
import json

# 协议定义
PRTL_DL645 = 1
PRTL_CJ188 = 2
PRTL_MODBUS = 3
PRTL_3762 = 4
PRTL_3761 = 5
PRTL_W_GW = 6
PRTL_W_NW = 7
PRTL_W_ZDL = 8
PRTL_LYJSON = 9

global CuverIndex
global CuverList
CuverInfo = {"Index":0, "List":[]}


def serialSend(plan, data, self):
    if self != None:
        # 串口发送
        if ('NLY1502_LY_JSON' in plan):
            dataArray = self.uim.onSendData(data, _type="ascii")
        else:
            dataArray = self.uim.onSendData(data)
        if self.uid.flags["__isopen__"] is True:
            self.uid.serial.send(dataArray)

def CuverFonfig(start, num, density):
    cuverList = []
    tm_rng = pd.date_range(start, periods=num, freq='H')
    for i in range(len(tm_rng)):
        s = str(tm_rng[i])
        strend = s[2:4]+s[5:7]+s[8:10]+s[11:13]+s[14:16]
        if i > 0:
            # cuver = CuverFonfig(strstart, strend, 0, "0015")
            cuverList += [strstart + "#" + strend + "#" + density]
            #print(cuver)
        strstart = strend
    return cuverList

def loadCuverConfig():
    try:
        configFile = open("cuver.json")
        defaultConfig = json.load(configFile)
        print(defaultConfig)
    finally:
        if configFile:
            configFile.close()
            return defaultConfig

def SendMake(self, plan, flag, data, value, timeout, answer):
    if self.uid.flags["__isopen__"] is False:
        return

    if self.test["timeout"] > 0:
        self.test["timeout"] -= 0.1
        return

    if flag == '发送' or flag == 'Read' or flag == 'Set':
        # 曲线读配置文件发送
        if value == "config" and CuverInfo["Index"] == 0:
            cfg = loadCuverConfig()
            CuverInfo["List"] = CuverFonfig(cfg["start"], cfg["num"], cfg["density"])
            value = CuverInfo["List"][0]
            CuverInfo["Index"]+=1
        elif value == "config" and CuverInfo["Index"] > 0:
            if CuverInfo["Index"] < len(CuverInfo["List"]):
                value = CuverInfo["List"][CuverInfo["Index"]]
                CuverInfo["Index"] += 1
            elif CuverInfo["Index"] >= len(CuverInfo["List"]):
                self.test["Index"] += 1
                CuverInfo["Index"] = 0

        if ('NLY1502_LY_JSON' in plan) and (flag == 'Read' or flag == 'Set'):
            prtl = judgePrtl(plan)
            List = dict(zip([data], [value]))
            VList = []
            VList += [flag]
            VList += [List]
            senddata = prtl2Make(prtl, VList)
            print(senddata)
        elif flag == '发送':
            senddata = data
            print(senddata)

        # 显示 串口发送
        if self != None:
            mainlog = showinfo.addTimelog(senddata)
            self.uim.SendTextEdit.append(mainlog)
            showinfo.recLog(mainlog)

            # 串口发送
            serialSend(plan, senddata, self)

            # 保存发送帧，用于接收部分比对
            self.test["SendFrame"] = senddata
            self.test["Answer"] = answer

        if timeout == '':
            timeout = 3
        self.test["timeout"] = timeout
        print("SendProcess sendindex:", self.test["Index"] - 1)
        if CuverInfo["Index"] > 0:
            print("cuverindex:", CuverInfo["Index"] - 1)
    else:
        self.test["timeout"] = 0
        self.test["Index"] += 1


def RecvProcess(self, type):
    if not self.qRecv.empty():
        data = self.qRecv.get()

        if type == PRTL_LYJSON:
            try:
                data = data.decode("GBK")
                print(data)
            except UnicodeDecodeError as err:
                print(err)
                self.test["timeout"] = 3
                return

        if self != None:
            mainlog = showinfo.addTimelog(data)
            self.uim.RxTextEdit.append(mainlog)
            showinfo.recLog(mainlog)

        # 是否有报文， 解析成标准报文， 供收发界面显示
        senddata = self.test["SendFrame"]
        answer = self.test["Answer"]

        ret, value = prtlDealFrame(type, data, senddata, answer)
        if ret > 0 and value is not None and len(value) > 0:
            self.test["timeout"] = 0.5
            if self.test["Index"] < self.test["Num"]:
                self.uim.AnaTableWidget.setItem(self.test["Index"] - 1, 4, QTableWidgetItem(value))
                self.uim.AnaTableWidget.setItem(self.test["Index"] - 1, 5, QTableWidgetItem("合格"))


def SendProcess(self):
    if self.uid.flags["__isopen__"] is False:
        return

    if self.test["State"] == "start":
        self.test["Index"] = 0
        CuverInfo["Index"] = 0
    elif self.test["State"] == "stop" or self.test["State"] == "end":
        return
    else:
        pass

    if self.test["Index"] < self.test["Num"]:
        self.test["State"] = "runing"
        i = self.test["Index"]
        plan = self.uim.planComboBox.currentText()
        SendMake(self, plan, self.plan.flag[i], self.plan.log[i], self.plan.value[i], self.plan.timeout[i],
                 self.plan.answer[i])
    else:
        self.test["Index"] = 0
        self.test["State"] = "end"
        self.uim.startTestButton.setText("测试结束(串口)")


# 方法一：将要执行的方法作为参数传给Thread的构造方法
def action(self, type):
    cnt = 0
    while (1):
        cnt += 1
        RecvProcess(self, type)
        SendProcess(self)
        time.sleep(0.2)
        if cnt > 10:
            cnt = 0
            print("Downlink alive")


# 创建发送线程
def DownLinkThread(self):
    plan = self.uim.planComboBox.currentText()
    type = judgePrtl(plan)
    t = threading.Thread(target=action, args=(self, type))
    t.start()



if __name__ == '__main__':
    plan = '6'
    num = 10
    flag = '发送'
    data = '68 12 34 56 78 90 16'
    timeout = 1

    # DownLinkThread(self=plan)


    num = 60
    start = "201812201234"
    end = "201812240000"
    density = "0015"

    '''
    tm_rng = pd.date_range('201812201250', periods=5, freq='H')
    for i in range(len(tm_rng)):
        s = str(tm_rng[i])
        strend = s[:4]+s[5:7]+s[8:10]+s[11:13]+s[14:16]
        if i > 0:
            cuver = CuverFonfig(strstart, strend, 0, "0015")
            print(cuver)
        strstart = strend
    '''
    str = CuverFonfig(start, num, density)
    for s in range(len(str)):
        print(str[s])