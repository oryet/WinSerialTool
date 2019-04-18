# -*- coding: cp936 -*-
import os
import xlrd

'''
print ('***获取当前目录***')
print (os.getcwd())
print (os.path.abspath(os.path.dirname(__file__)))

print ('***获取上级目录***')
print (os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
print (os.path.abspath(os.path.dirname(os.getcwd())))
print (os.path.abspath(os.path.join(os.getcwd(), "..")))

print ('***获取上上级目录***')
print (os.path.abspath(os.path.join(os.getcwd(), "../..")))
'''

class ExcelPlan():
    def __init__(self, planText):
        if os.path.exists('plan\\'+planText + '.xls'):
            path = os.getcwd() + '\\plan\\' + planText + '.xls'
            wb = xlrd.open_workbook(path)

            SHEET_NUM = 0

            # 获得工作表的方法1
            sh = wb.sheet_by_index(SHEET_NUM)

            # 获得行数
            self.row_count = sh.nrows
            # print(row_count)

            # 获得列数
            self.col_count = sh.ncols
            # print(col_count)

            # 初始化
            self.name = ['']*self.row_count
            self.flag = ['']*self.row_count
            self.log = ['']*self.row_count
            self.timeout = ['']*self.row_count
            self.answer = ['']*self.row_count
            self.value = [''] * self.row_count

            if self.col_count >= 1:
                self.name = sh.col_values(0)
            if self.col_count >= 2:
                self.flag = sh.col_values(1)
            if self.col_count >= 3:
                self.log = sh.col_values(2)
            if self.col_count >= 4:
                self.timeout = sh.col_values(3)
            if self.col_count >= 5:
                self.value = sh.col_values(4)
            if self.col_count >= 6:
                self.answer = sh.col_values(5)
        else:
            self.row_count = 0
            self.col_count = 0


    def Name(self, i):
        return  self.name[i]

    def NameList(self):
        return  self.name

    def Flag(self, i):
        if self.flag[i] == '发送':
            return True
        else:
            return False

    def FlagList(self):
        return  self.flag

    def Cmd(self, i):
        return self.flag[i]

    def Data(self, i):
        return self.log[i]

    def DataList(self):
        return self.log

    def Timeout(self, i):
        return self.timeout[i]

    def TimeoutList(self):
        return self.timeout

    def Answer(self, i):
        return self.answer[i]

    def AnswerList(self):
        return self.answer

    def Num(self):
        return self.row_count

    def Value(self, i):
        return self.value[i]

    def ValueList(self):
        return self.value

if __name__ == '__main__':
    ep = ExcelPlan("TLY2807_I_LY_W_NW")
    print(ep.Answer(1))