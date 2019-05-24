# coding:utf-8
import threading
import time
from PublicLib.Protocol.protocol import judgePrtl
from PublicLib.Protocol.protocol import prtl2Frame


def serialSendAndPrint(plan, data, self):
    dataArray = self.uim.onSendData(data)
    if self != None:
        self.uid.serial.send(dataArray)
    dt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    byteStr = dt + ': ' + data
    if self != None:
        self.uim.SendTextEdit.append(byteStr)
        prtl = judgePrtl(plan)
        (ret, addr, ctrl, data) = prtl2Frame(prtl, data)
        if ret:
            print(addr, ctrl, data)


# 方法一：将要执行的方法作为参数传给Thread的构造方法
def action(plan, num, flag, data, timeout, self):
    for i in range(num):
        if flag[i] == '发送':
            print('the num is:%s\r' % i)
            print('the data is:%s\r' % data[i])
            serialSendAndPrint(plan, data[i], self)

            if timeout[i] == '':
                timeout[i] = 3
            time.sleep(timeout[i])
        else:
            continue



#创建发送线程
def sendThread(plan, num, flag, data, timeout, self):
    t = threading.Thread(target=action, args=(plan, num, flag, data, timeout, self))
    t.start()

if __name__ == '__main__':
    plan = '645'
    num = 10
    flag = '发送'
    data = '68 12 34 56 78 90 16'
    timeout = 1
    sendThread(plan, num, flag, data, timeout, self=None)

