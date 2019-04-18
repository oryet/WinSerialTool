import threading
from time import sleep
from serial import Serial
import logging
from PyQt5.QtCore import pyqtSignal, QObject

logger = logging.getLogger('main.StSerial')


class StSerial(QObject, threading.Thread):
    received = pyqtSignal(bytes)
    def __init__(self):
        super(StSerial, self).__init__()
        # threading.Thread.__init__(self)
        self.__terminate = None
        logger.info('DsSerial Logger Start')

    @staticmethod
    def searchSerialPort():
        ''' Search the valid serial port '''
        ports = []
        for i in range(100):
            port = 'COM' + str(i + 1)
            try:
                s = Serial(port)
                if s.isOpen():
                    s.close()
                ports.append(port)
                logger.info("Found :" + port)
            except Exception as msg:
                pass
        return ports

    def open(self, settings):
        try:
            self.serial = Serial(settings['port'], settings['baud'],
                                 settings['bytesize'], settings['parity'],
                                 settings['stopbits'], settings['timeout'])
            self.serial.flushInput()
            self.serial.flushOutput()
        except Exception as msg:
            logger.info('Port Open Failed :' + msg)
        logger.info('Port Opened Successful')
        return True, 'Successful'

    def getPort(self):
        print(self.serial)

    def terminate(self, flag):
        self.__terminate = flag;

    def send(self, data):
        if self.serial.isOpen():
            try:
                self.serial.write(data)
            except Exception as msg:
                logger.info("Port write failed :" + msg)
        else:
            logger.error('Port Not Open')

    def __recv(self):
        data, quit = None, False
        while True:
            if self.__terminate == False:
                self.serial.close()
                break
            data = self.serial.read(1)
            sleep(0.1)
            if data == b'':
                continue
            while True:
                n = self.serial.inWaiting()
                if n > 0:
                    data += self.serial.read(n)
                    sleep(0.1)
                else:
                    quit = True
                    break
            if quit:
                break
        return data

    def close(self):
        #if self.serial.isOpen():
        self.serial.close()

    def run(self):
        while 1:
            data = self.__recv()
            if not data:
                break
            self.received.emit(data)
        self.serial.close()