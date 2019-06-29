
# 客户端 Client

from os import _exit
from getpass import getpass
from socket import *
import threading, time, signal

coding = 'utf-8'
flag = False
data = 'q'

# 用于功能选择
def menu(signum, frame):
    global flag, data
    flag = True
    print('\nq    ---程序退出。')
    while True:
        if threading.active_count() == 2 or threading.active_count() == 1:
            break
        else:
            time.sleep(0.01)
    if data == 'q':
        _exit(0)
    flag = False
    sendThread = threading.Thread(target=sendDog, args=(aims,))
    sendThread.start()


# 接收信息
def recv():
    while True:
        data = client.recv(1024)
        if not data:
            break
        if len(data)<1024:
            print(data.decode(coding))
            continue
        else:
            print(data.decode(coding),end='')
    print('连接已断开')
    client.close()
    _exit(0)


# 守护 消息狗
def sendDog(aims):
    _send = threading.Thread(target=send, args=(aims,))
    _send.start()
    while True:
        if flag:
            break
        else:
            time.sleep(0.05)


def send(aims):
    global data
    # 发送目标
    client.send(aims.encode(coding))
    while True:
        try:
            # 输入消息
            data = input()
            if flag:
                break
            client.send(data.encode(coding))
        except:
            break


# 注册
def signUp():
    client.send('Y'.encode(coding))
    time.sleep(0.01)
    client.send(input('用户名： ').encode(coding))
    time.sleep(0.01)
    client.send(getpass('密码： ').encode(coding))


def main():
    global client
    serverIP = '0.0.0.0'
    port = 1027
    # 创建套接字
    client = socket(AF_INET, SOCK_STREAM)
    for i in range(10):
        try:
            client.connect((serverIP, port))
            break
        except ConnectionRefusedError:
            port = port + 1
        if i == 9:
            print('无法连接服务器')
            _exit(0)

    # 发送用户名
    while True:
        userName = input('用户名：')
        # userName='hyx'
        client.send(userName.encode(coding))
        signinfo = client.recv(1)
        if int(signinfo.decode(coding)) == 0:
            print('用户不存在')
            if input('是否注册？(Y/N) ') == 'Y':
                signUp()
            else:
                client.send('N'.encode(coding))
                continue
        break

    print('已连接服务器。')

    aims = input('联系人名：')
    # aims = 'hyx'

    # 新建线程 接收信息
    recvThread = threading.Thread(target=recv)
    recvThread.start()

    # 新建线程 发送信息
    sendThread = threading.Thread(target=sendDog, args=(aims,))
    sendThread.start()

    recvThread.join()

# 信号处理
signal.signal(signal.SIGINT, menu)


if __name__ == '__main__':
    main()
