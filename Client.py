#!/usr/bin/python3

# 客户端 Client

from socket import *
import threading, time, signal, os, _thread


#======================================
coding = 'utf-8'
flag = True
#======================================


# 用于功能选择
def menu(signum, frame):
    flag == False
    print('exit    ---程序退出。')
    data = input('选：')
    if data == 'exit':
        client.close()
        os._exit(0)
        return 0
    ts = threading.Thread(target=sendMess)
    ts.start()
    # client.close()
    # os._exit(0)

# 接收信息
def recv():
    while True:
        print('收：',end='')
        # print('[%s:]' % contact,end='')
        data = client.recv(1024)
        if not data:
            break
        if len(data)<1024:
            print(data.decode(coding))
            continue
        else:
            print(data.decode(coding),end='')
    print('连接已断开\n按回车退出')
    client.close()
    os._exit(0)


# 发送信息
def sendDog():
    print(_thread.start_new_thread(sendMess,()))
    while True:
        if flag == False:
            break
        else:
            time.sleep(0.05)

def sendMess():
    while True:
        # 发送目标
        client.send(aims.encode(coding))
        try:
            # 输入消息
            data = input('发')
            client.send(data.encode(coding))
            print('已发送')
        except:
            break


# 注册
def signUp():
    client.send('Y'.encode(coding))
    time.sleep(0.01)
    client.send((input('用户名： ')).encode(coding))
    time.sleep(0.01)
    client.send((input('密码： ')).encode(coding))


def main():
    global client
    serverIP = ('127.0.0.1',1027)
    # 创建套接字
    client = socket(AF_INET, SOCK_STREAM)
    client.connect(serverIP)

    global aims
    # 发送用户名
    while True:
        userName = input('用户名：')
        # userName='zys'
        client.send(userName.encode(coding))
        data = client.recv(1)
        if int(data.decode(coding)) == 1:
            break
        else:
            print('用户不存在')
            if input('是否注册？(Y/N) ') == 'Y':
                signUp()
    print('已连接服务器。')

    aims = input('联系人名：')
    # aims = 'hyx'
    # funcopt='choosefriend'
    # client.send(funcopt.encode(coding))
    # time.sleep(0.01)
    # menu[funcopt]()

    # 新建线程 接收信息
    tr = threading.Thread(target=recv)
    tr.start()
    # 新建线程 发送信息
    ts = threading.Thread(target=sendDog)
    ts.start()

    tr.join()



# 信号处理
signal.signal(signal.SIGINT, menu)
signal.signal(signal.SIGTERM, exit)

if __name__ == '__main__':
    main()
