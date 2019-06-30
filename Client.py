
# 客户端 Client

from os import _exit
from getpass import getpass
from socket import *
import threading, time, sys, signal, hashlib

coding = 'utf-8'
flag = False
data = 'q'

# 创建套接字
client = socket(AF_INET, SOCK_STREAM)

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


def _getpass():
    passwd = getpass('输入密码: ')
    passwd = hashlib.md5(passwd.encode(coding)).hexdigest()
    return passwd.encode(coding)


# 注册
def signUp():
    client.send('Y'.encode(coding))
    while True:
        client.send(input('用户名： ').encode(coding))
        if client.recv(1).decode(coding) == '0':
            print('用户已存在')
            continue
        break
    for x in range(3):
        passwd = _getpass()
        print('再次',end='')
        sys.stdout.flush()
        if _getpass() == passwd:
            break
        if x == 2:
            print('注册失败')
            return False
    print('注册成功')
    client.send(passwd)


# 连接服务器
def connectserver():
    print('正在连接服务器')
    try:
        with open('ServerIP','r') as IPfile:
            for i in IPfile:
                port = 1027
                serverIP = i.strip('\n')
                if serverIP == '###':
                    print('无法连接ServerIP文件中已有的服务器')
                    print('请检查ServerIP文件')
                    _exit(0)
                print('尝试连接 {}'.format(serverIP))
                for i in range(10):
                    socketerror = client.connect_ex((serverIP, port))
                    if socketerror == 0:
                        break
                    else:
                        port = port + 1
                    if i == 9:
                        print('无法连接 {}'.format(serverIP))
                if socketerror == 0:
                    break
    except FileNotFoundError:
        print('无ServerIP文件，请创建并填写服务器IP')
        _exit(0)
    print('连接成功')


def signIn():
    # 发送用户名
    while True:
        client.send(input('用户名：').encode(coding))
        if client.recv(1).decode(coding) == '0':
            print('用户不存在')
            if input('是否注册？(Y/N) ') == 'Y':
                signUp()
                continue
            else:
                client.send('N'.encode(coding))
                continue
        break
    # 发送密码（3次机会）
    for x in range(3):
        client.send(_getpass())
        if client.recv(1).decode(coding) == '0':
            print('密码错误！')
        else:
            break
        if x == 2:
            return False
    return True


def main():
    # 连接服务器
    connectserver()

    if not signIn():
        return 0

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
