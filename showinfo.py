# coding:utf-8
import time
import logging
from PublicLib.Protocol.protocol import judgePrtl
from PublicLib.Protocol.protocol import prtl2Frame


def addTimelog(log):
    dt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return dt + ': ' + log


def showMainlog(log):
    timelog = addTimelog(log)
    return timelog


def planana(plan, log):
    prtl = judgePrtl(plan)
    l = prtl2Frame(prtl, log)
    return l


def recLog(l):
    logger = logging.getLogger('showinfo')
    logger.info(str(l))


def showAnalog(log, plan, logen):
    analog = showMainlog(log)
    l = planana(plan, log)
    if l[0]:
        analog += "\n报文分析:\n"
        for i in range(1, len(l)):
            analog += str(l[i]) + "\n"
    analog += "\n\n"

    if logen and l[0]:
        recLog(log)
        recLog(str(l))
    return analog, l

def findAna(a, s):
    start = 0
    end = 0
    flag = s
    la = []
    for i in range(a.count(flag)):
        end = a.find(flag, start)
        la += [a[start:end]]
        start = end + 1
    return la

def judgeAna(l, la):
    cnt = 0
    n = len(la)
    for i in range(n):
        if la[i] in l:
            cnt += 1
    if cnt == n:
        return True
    else:
        return False

def judgeAnaList(l, a):
    la = findAna(a, ',')
    return judgeAna(l, la)

def cmpc(s):
    n = s.find('%')
    if (n >= 0):
        c = s[n + 1:]
        return 1, int(c, 10)  # 百分比输入
    else:
        return 0, int(s, 10)  # 数据输入


def cmpdate(s, d, m, a, c):
    if (m == 'year'):
        pass
    elif (m == 'month'):
        pass
    elif (m == 'day'):
        pass
    elif (m == 'hour'):
        pass
    elif (m == 'minute'):
        pass
    elif (m == 'second'):
        pass
    elif (m == 'data'):
        sd = float(s)
        dd = float(d)
        dmax = dmin = 0
        if (a):
            if (c <= 100):
                dmax = dd * (1 + c / 100)
                dmin = dd * (1 - c / 100)
        else:
            dmax = dd + c
            dmin = dd - c
        if dmin <= sd <= dmax:
            return True
        else:
            return False

def judgeAnaList2(l, a):
    la = findAna(a, ':')
    a, c = cmpc(la[2])
    f = cmpdate(l, la[1], la[0], a, c)
    return f

if __name__ == '__main__':
    # a = '目标地址:FFFFFFFFFFFF,源地址:010004030201,MAC信标帧,'
    # l = [True, '20', '00', '00', '帧长度:37', '信道索引号:0', 'panid:FFFF', '目标地址:FFFFFFFFFFFF', '源地址:010004030201', 'MAC信标帧', '发射随机延时:40', '信标轮次:1', '层次号:1', '信标轮次限值:8', '层次号限:8', '时隙号:0E00', '信标标识:3F', '网络规模:1A00', '场强门限:60', '中心节点私有信道组号:06', '中心节点 PANID:3D06']

    l = '220.0'
    s1 = 'data:220:10:,'  # 数据判断 210~230 都算合格
    s2 = 'data:220:%10:,'  # 数据判断 198~242 都算合格
    a = s1

    b = judgeAnaList2(l, a)
    print(b)

