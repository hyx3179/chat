
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
def pack(uid, message):
    return (str(int(uid))+message).encode(coding)


# 接收信息
def recv(sock):
    while True:
        data = sock.recv(1024)
        # 解码
        message=data.decode(coding)
        # 拆包
        message=message[1:]
        # 打印消息
        print(time.asctime( time.localtime(time.time())))
        print('[%s:] %s' % (contact, message))

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
            global uid
            message = pack(uid, message)
            sock.send(message)
        except:
            break


def main():
    # 信号处理
    signal.signal(signal.SIGINT, exit)
    signal.signal(signal.SIGTERM, exit)

    global userName, contact, uid
    # 发送用户名
    # userName = input('用户名：')
    userName='zys'
    client.send(userName.encode(coding))
    uid = client.recv(1)
    # 发送联系人名
    # contact = input('联系人名：')
    contact = 'hyx'
    client.send(contact.encode(coding))

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
