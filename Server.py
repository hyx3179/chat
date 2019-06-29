
# 服务器 Server

from os import _exit
from socket import *
import threading, time, signal
import dbOpt

port = 1027

# 创建套接字
server = socket(AF_INET, SOCK_STREAM)
for i in range(10):
    try:
        print(port)
        server.bind(('0.0.0.0', port))
        break
    except OSError:
        port = port + 1
    if i == 9:
        _exit(0)

server.listen()

coding = 'utf-8'
sockDict = {}


# 用于正常退出程序
def exit(signum, frame):
    print('服务器关闭。')
    server.close()
    _exit(0)
# 信号处理
signal.signal(signal.SIGINT, exit)

def signUp(sock):
    newUser = sock.recv(20).decode(coding)
    time.sleep(0.01)
    passwd = sock.recv(64).decode(coding)
    dbOpt.insert('userInfo',newUser,passwd)
    print('新用户：%s'%newUser)


# 转发消息
def transfer(sock, userName):
    while True:
        aims = sock.recv(20).decode(coding)
        if not aims:
            return 0
        while True:
            try:
                sender = sockDict[aims]
                break
            except KeyError:
                try:
                    sock.send('目标未上线'.encode(coding))
                    time.sleep(1)
                except BrokenPipeError:
                    return 0
        while True:
            data = sock.recv(1024)
            print(data)
            if not data:
                break
            sender.send(userName.encode(coding))
            sender.send(data)


def client(sock):
    while True:
        # 接受用户名
        userName = sock.recv(20).decode(coding)
        # 用户断开链接
        if not userName:
            print('%s 断开链接' % sock)
            sock.close()
            return 0
        # 用户不存在返回0 提示 注册
        result = dbOpt.selectuName('userInfo', userName)
        if  result == 0:
            sock.send('0'.encode(coding))
            if sock.recv(1).decode(coding) == 'Y':
                # 注册函数
                signUp(sock)
            else:
                continue
            continue
        else:
            sock.send('1'.encode(coding))
            # 保存客户端信息
            sockDict[userName]=sock
            break

    print('%s 已连接.' % userName)

    transfer(sock, userName)

    sock.close()
    print('%s 断开链接' % userName)
    # 删除要关闭的客户端
    del sockDict[userName]


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

