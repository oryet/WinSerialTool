# -*- coding: utf-8 -*-
from Protocol.dl645 import deal645Frame
from Protocol.cj188 import deal188Frame
from Protocol.w_nw import wnwdealframe
from Protocol.packagetool import pt4_dealframemain
import Protocol.ly_Json as jsonframe
import showinfo

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


# 协议判断
def judgePrtl(plan):
    plan = plan.upper()  # 字符串转大写
    prtl = 0

    # print(plan.find('645'))

    if plan.find('645') >= 0:
        prtl = PRTL_DL645
    elif plan.find('188') >= 0:
        prtl = PRTL_CJ188
    elif plan.find('MODBUS') >= 0:
        prtl = PRTL_MODBUS
    elif plan.find('3762') >= 0 or plan.find('376.2') >= 0:
        prtl = PRTL_3762
    elif plan.find('3761') >= 0 or plan.find('376.1') >= 0:
        prtl = PRTL_3761
    elif plan.find('W_GW') >= 0:
        prtl = PRTL_W_GW
    elif plan.find('W_NW') >= 0:
        prtl = PRTL_W_NW
    elif plan.find('W_ZDL') >= 0:
        prtl = PRTL_W_ZDL
    elif plan.find('JSON') >= 0:
        prtl = PRTL_LYJSON
    return prtl


# 协议解帧
# 返回格式定义： 是否正确， 地址域， 控制字， 数据区
def prtl2Frame(prtl, frame):
    if prtl == PRTL_LYJSON:
        l = [False]  # JsonParse(frame)
        return l

    frame = frame.replace(' ', '')
    frame = frame.lower()

    # 协议解析
    if prtl == PRTL_DL645:
        l = deal645Frame(frame)
    elif prtl == PRTL_CJ188:
        l = deal188Frame(frame)
    elif prtl == PRTL_W_NW:
        l = pt4_dealframemain(frame)
        if l[0]:
            l = l[:-2] + wnwdealframe(l[-1])
    return l


def prtl2Make(prtl, frame):
    # 组帧
    if prtl == PRTL_LYJSON:
        frame = jsonframe.JsonMakeFrame(frame)
    return frame

def prtlDealFrame(type, data, senddata, answer):
    if type == PRTL_LYJSON:
        return jsonframe.JsonDealFrame(data, senddata, answer)
    else:
        pass

def prtlDealFrameA(mode, data, self, type):
    if type == PRTL_LYJSON:
        if mode == 'serial':
            try:
                data = data.decode("GBK")
            except UnicodeDecodeError as err:
                print(err)
                return -1

        return data

        log = showinfo.addTimelog(data)
        self.uim.RxTextEdit.append(log)
        showinfo.recLog(log)

        # 解析
        # self.uim.AnaTableWidget.setItem(self.uim.sendIndex, 5, QTableWidgetItem("合格"))

        # 显示
        # self.uim.AnaTableWidget.setItem(i, 3, QTableWidgetItem(self.plan.Value(i)))
        return 0
    else:
        data = ' '.join(["%02X" % x for x in data])
        # self.ep = ExcelPlan(plan)
        sendIndex = self.sendIndex

        senddata = self.ep.Data(sendIndex)
        senddata = senddata.upper()
        nfind = data.find(senddata)

        if (nfind >= 0):
            data = data[nfind + len(senddata):]
        elif (nfind < 0):
            return 0
        if (len(data) < 5):
            return 0
    log = showinfo.addTimelog(data)
    self.RxTextEdit.append(log)

    name = self.ep.Name(sendIndex)
    if type == PRTL_LYJSON and nfind >= 0:
        analog = data[nfind + len(senddata):-2]
        self.textEdit_a.append(analog)
    else:
        # (log, l) = showinfo.showAnalog(data, plan, 1)
        pass

    if (l[0]):
        log = name + ':\n' + log
        self.textEdit_a.append(log)

        # 帧合法性判断
        la = self.ep.Answer(sendIndex)
        if (len(la) > 0):
            b = showinfo.judgeAnaList(l, la)
            strinfo = name + ': ' + str(b) + '\n\n'
        else:
            strinfo = name + '\n\n'
        self.textEdit_m.append(strinfo)
    return 0

if __name__ == '__main__':

    frame = 'FE FE aa aa 68 22 22 22 22 22 22 68 93 06 55 55 55 55 55 55 33 16'
    '''

    frame = "68 20 39 00 00 00 17 33 00 33 01 0C 25 FF FF 09 00 00 55 07 00 01 00 04 03 02 01 01 0C 09 00 00 55 07 " \
            "00 01 00 04 03 02 01 21 11 10 02 09 00 00 55 07 00 32 58 29 08 70 41 20 59 65 B7 16"
    '''
    '''
    frame = '68 20 34 00 00 00 19 2E 00 2E 01 0C EA 3D 06 58 29 08 70 41 20 01 00 04 03 02 01 80 0C 58 29 08 70 41 20 09 00 00 55 07 00 A1 01 03 01 00 04 03 02 01 01 EA 08 00 63 33 16 68 20 3C 00 00 00 62 36 00 36 01 0C 40 3D 06 01 00 04 03 02 01 58 29 08 70 41 20 80 0C 09 00 00 55 07 00 58 29 08 70 41 20 A2 11 03 01 00 04 03 02 01 11 EA 08 10 01 58 29 08 70 41 20 00 7B E0 16 68 20 3C 00 00 00 1C 36 00 36 01 0C EB 3D 06 09 00 00 55 07 00 01 00 04 03 02 01 80 0C 09 00 00 55 07 00 58 29 08 70 41 20 A1 01 03 01 00 04 03 02 01 11 EA 08 10 01 58 29 08 70 41 20 00 C3 BC 16'
    '''

    prtl = judgePrtl('645')
    print(prtl)
    l = prtl2Frame(prtl, frame)
    if l[0]:
        print(l[1:])
