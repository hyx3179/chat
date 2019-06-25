
# 客户端 Client

from socket import *
import threading, time, signal, os

serverAddr = ('127.0.0.1',1027)
# 创建套接字
client = socket(AF_INET, SOCK_STREAM)
client.connect(serverAddr)
coding = 'utf-8'


# 用于正常退出程序
def exit(signum, frame):
    print('程序退出。')
    client.close()
    os._exit(0)


# uid 为 int 
def pack(id, message):
    return (str(id)+message).encode(coding)



# 接收信息
def recv(sock):
    while True:
        print(time.asctime( time.localtime(time.time())))
        print('[%s:]' % contact,end='')
        while True:
            data = sock.recv(1024)
            if len(data)<1024:
                print(data.decode(coding),end='')
                break
            else:
                print(data.decode(coding),end='')
                # continue
        if not data:
            break
    print('连接已断开\n按回车退出')
    sock.close()
        

# 发送信息
def sendMess(sock):
    while True:
        try:
            # 输入消息
            message = input()
            # 打包
            global cid
            message = pack(cid, message)
            sock.send(message)
        except:
            break


def main():
    # 信号处理
    signal.signal(signal.SIGINT, exit)
    signal.signal(signal.SIGTERM, exit)

    global userName, contact, cid
    # 发送用户名
    # userName = input('用户名：')
    userName='hyx'
    client.send(userName.encode(coding))
    # 发送联系人名
    # contact = input('联系人名：')
    contact = 'zys'
    client.send(contact.encode(coding))
    cid = client.recv(1)

    print('已连接服务器。')
    # 新建线程 接收信息  发送信息
    tr = threading.Thread(target=recv, args=(client,))
    ts = threading.Thread(target=sendMess, args=(client,))
    tr.start()
    ts.start()

    tr.join()
    ts.join()


if __name__ == '__main__':
    main()
