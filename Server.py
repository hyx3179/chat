#!/usr/bin/python3

# 服务器 Server

from socket import *
import threading, time, signal, os
import dbOpt

serverIP = ('127.0.0.1',1027)

# 创建套接字
server = socket(AF_INET, SOCK_STREAM)
server.bind(serverIP)
server.listen(5)

#======================================
coding = 'utf-8'
uidtable = {}
menu = {}
conTuple = {}
relationList={}
#=====================================


# 用于正常退出程序
def exit(signum, frame):
    print('服务器关闭。')
    server.close()
    os._exit(0)
# 信号处理
signal.signal(signal.SIGINT, exit)
signal.signal(signal.SIGTERM, exit)


def signUp(sock):
    newUser = sock.recv(20)
    time.sleep(0.01)
    passwd = sock.recv(64)
    dbOpt.insert('userInfo',newUser,passwd)
    print('新用户：%s'%newUser)

# 转发消息
def transfer(sock):
    while True:
        aims = sock.recv(20).decode(coding)
        while True:
            try:
                sender = conTuple[aims]
                break
            except KeyError:
                sock.send('目标未上线'.encode(coding))
                time.sleep(0.5)
        while True:
            data = sock.recv(1024)
            if not data:
                break
            if len(data)<1024:
                sender.send(data)
                continue
            else:
                sender.send(data)


def client(sock):
    while True:
        # 接受用户名
        userName = sock.recv(20)
        # 用户断开链接
        if not userName:
            return 0
        userName = userName.decode(coding)
        result = dbOpt.selectuName('userInfo', userName)
        # 用户不存在返回0 提示 注册
        if  result == 0:
            sock.send('0'.encode(coding))
            if sock.recv(1).decode(coding) == 'Y':
                # 注册函数
                signUp(sock)
            continue
        else:
            sock.send('1'.encode(coding))
            # 保存客户端信息
            conTuple[userName]=sock
            break
    print('%s 已连接.' % userName)
    # # 功能选择
    # funcopt = sock.recv(20)
    # cid = menu[funcopt.decode(coding)](sock)

    # while True:
    #     try:
    #         sender = conTuple[cid]
    #         break
    #     except KeyError:
    #         time.sleep(0.1)
    #         continue

    transfer(sock)

    sock.close()
    print('%s 断开链接' % userName)
    # 删除要关闭的客户端
    del conTuple[userName]


def main():
    print('等待连接...')
    while True:
        # 链接客户端
        sock = server.accept()[0]
        # 新建线程 接收信息  发送信息
        thread = threading.Thread(target=client, args=(sock,))
        thread.start()


if __name__ == '__main__':
    main()

