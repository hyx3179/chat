
# 服务器 Server

from os import _exit
from socket import *
import threading, time, signal
import DBManager

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
    print('服务器关闭。') # 日志
    server.close()
    _exit(0)
# 信号处理
signal.signal(signal.SIGINT, exit)


def signUp(sock):
    while True:
        newUser = sock.recv(20).decode(coding)
        # 查询用户是否存在
        # 存在
        if DBManager.existent(newUser):
            sock.send('0'.encode(coding))
            continue
        # 不存在 发送1 接收密码
        sock.send('1'.encode(coding))
        passwd = sock.recv(32).decode(coding)
        DBManager.insert('userInfo',newUser,passwd)
        print('新用户：%s'%newUser) # 日志
        break


def signIn(sock):
    while True:
        # 接受用户名
        try:
            userName = sock.recv(20).decode(coding)
        # Windows 用户断开链接
        except ConnectionResetError:
            return sock
        # Linux 用户断开链接
        if not userName:
            return sock
        # 用户不存在返回False 提示 注册
        if not DBManager.existent(userName):
            sock.send('0'.encode(coding))
            if sock.recv(1).decode(coding) == 'Y':
                # 注册函数
                signUp(sock)
            continue
        else:
            sock.send('1'.encode(coding))
            break
    for x in range(3):
        # 等待登陆密码
        signInPasswd=sock.recv(32).decode(coding)
        # 匹配登陆密码
        match = DBManager.match(userName, signInPasswd)
        if match:
            sock.send('1'.encode(coding))
            break
        sock.send('0'.encode(coding))
        if x == 2:
            return sock
    # 保存客户端信息
    sockDict[userName]=sock
    return userName

# 转发消息
def transfer(sock, userName):
    while True:
        # 接受目标信息
        try:
            aims = sock.recv(20).decode(coding)
        # Windows 用户断开链接
        except ConnectionResetError:
            return 0
        # Linux 用户断开链接
        if not aims:
            return 0
        # 检差目标状态
        while True:
            try:
                sender = sockDict[aims]
                break
            except KeyError:
                try:
                    sock.send('目标未上线'.encode(coding))
                    time.sleep(1)
                # 用户断开链接
                except (BrokenPipeError, ConnectionResetError):
                    return 0
        while True:
            # 接受数据
            try:
                data = sock.recv(1024)
                print(data) # 存入聊天记录数据库
            # Windows 用户断开链接
            except ConnectionResetError:
                return 0
            # Linux 用户断开链接
            if not data:
                return 0
            # 发送数据
            try:
                sender.send(userName.encode(coding))
                sender.send(data)
            # 目标下线
            except OSError:
                sock.send('目标下线'.encode(coding))
                break


def client(sock):
    # 接收连接信息
    userName = signIn(sock)
    if isinstance(userName, str):
        print('%s 已连接.' % userName) # 日志
        # 开始转发数据
        transfer(sock, userName)
        # 删除要关闭的客户端
        del sockDict[userName]

    print('%s 断开链接' % userName) # 日志
    sock.close()


def main():
    print('等待连接...') # 日志
    while True:
        # 链接客户端
        sock = server.accept()[0]
        # 新建线程 接收信息  发送信息
        thread = threading.Thread(target=client, args=(sock,))
        thread.start()


if __name__ == '__main__':
    main()

