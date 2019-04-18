import socketserver
import threading
import queue
import time
import logging.config
import logging
import json
from ConnManage import ConnManage

q = queue.Queue()
server = None
MAX_LIVE_TIME = (10*60*60)  # 1小时

global con
con = ConnManage()

class Myserver(socketserver.BaseRequestHandler):
    def handle(self):
        conn = self.request
        # 加入连接池
        con.Insert(conn, self.client_address[0], self.client_address[1], MAX_LIVE_TIME)
        print("link ip:", str(self.client_address[0]), "port:", str(self.client_address[1]))

        while True:
            time.sleep(0.1)
            try:
                ret_bytes = conn.recv(2048)
                ret_str = str(ret_bytes, encoding="utf-8")
                if len(ret_str) > 5:
                    # print("{} wrote:".format(self.client_address[0]))
                    # print("from conn:", conn)
                    # print(ret_str)
                    recvdata = str(self.client_address[0]) + ',' + str(self.client_address[1]) + ':' + ret_str
                    con.Updata(conn, self.client_address[0], self.client_address[1], MAX_LIVE_TIME)
                    q.put(recvdata)
                    if 'Login' in ret_str or 'Heart' in ret_str or 'Event' in ret_str:
                        conn.sendall(bytes(ret_str+" ",encoding="utf-8"))
                elif len(ret_str) == 0:
                    self.remove()
                    break
            except:  # 意外掉线
                self.remove()
                break

    def finish(self):
        print("client remove!")

    def remove(self):
        print("client offline!", self.request)
        con.Delect(self.request)

def SocketSend(n, data):
    if 0 < con.GetLinkNum():
        if n < con.GetLinkNum():
            conn = con.GetConn(n)
            conn.sendall(bytes(data + " ", encoding="utf-8"))

def ServerMonitor(qRecv):
    linkNum = 0
    while True:
        time.sleep(0.1)
        con.Live()

        if linkNum != con.GetLinkNum():
            linkNum = con.GetLinkNum()
            data = "当前连接数：" + str(linkNum)
            qRecv.put(data)
            # print("当前连接数：", linkNum)

        # if len(recvdata) > 5:
        while not q.empty():
            data = q.get()
            qRecv.put(data)
            print(data)

# 获取链接数量
def GetLinkNum():
    return con.GetLinkNum()


# 获取链接端口信息
def GetPoolPortList():
    return con.GetIpPortList()


# 获取链接IP信息
def GetPoolAddrList():
    return con.GetIpList()


def ServerClose():
    server.shutdown()
    server.server_close()

def ServerStart(ADDRESS):
    global server
    server = socketserver.ThreadingTCPServer(ADDRESS, Myserver)
    server.serve_forever()
    return

'''
def loggingConfig():
    logging.config.fileConfig('loggingsocket.conf')
    #root_logger = logging.getLogger('root')
    #root_logger.debug('Logging System Start')
    logger = logging.getLogger('main')
    logger.info('Logging main Start')

def loadSocketDefaultSettings():
    try:
        socketConfigFile = open("socket.json")
        defaultSocketConfig = json.load(socketConfigFile)
        print(defaultSocketConfig)
    finally:
        if socketConfigFile:
            socketConfigFile.close()
            return defaultSocketConfig
'''

if __name__ == "__main__":
    ADDRESS = ('192.168.127.16', 8888)
    # loggingConfig()
    # defaultSocketConfig = loadSocketDefaultSettings()
    # ip = defaultSocketConfig['ip']
    # ipport = defaultSocketConfig['ipport']
    # ADDRESS = (ip, ipport)
    # logger = logging.getLogger('main')
    # logger.info(ADDRESS)
    t = threading.Thread(target=ServerMonitor, args=(None))
    t.start()
    server = socketserver.ThreadingTCPServer(ADDRESS, Myserver)
    server.serve_forever()
