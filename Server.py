
# 服务器 Server

from socket import *
import threading, time, signal, os

coding = 'utf-8'

server = socket(AF_INET, SOCK_STREAM)
server.bind(('0.0.0.0', 1027))
server.listen(5)
print('等待连接...')


#======================================
uidtable = {'zys':1, 'hyx':2}
conTuple = {}
relationList={}
##=====================================


# 用于正常退出程序
def exit(signum, frame):
    print('服务器关闭。')
    os._exit(0)


signal.signal(signal.SIGINT, exit)
signal.signal(signal.SIGTERM, exit)

# uid 为 int 
def pack(uid, message):
    return (str(uid)+message).encode(coding)


# 拆信息
def getCid(message):
        return int(message[0])

    
   
# 发送客户端信息
def sendInfo(sock, addr):
    ipInfo = pack(str(addr[0]),str(addr[1]), 0,str(addr))
    sock.send(ipInfo)
    
    
# 保存客户端信息
def save(sock, id):
    # conList.append(id)
    conTuple[id]=sock


# 删除要关闭的客户端
def drop(id):
    global conTuple
    # del conList[conList.index(id)]
    del conTuple[id]


# 转发消息
def transmit(sock, who):
    while True:
        data = sock.recv(1)
        if not data:
            break
        sender=conTuple[getCid(data)]
        while True:
            data = sock.recv(1024)
            if len(data)<1024:
                break
            else:
                sender.send(finMessage.encode(coding))
                # continue
        sender.send(finMessage.encode(coding))
        
    sock.close()
    print('%s 断开链接' % who)
        


def init(sock):
    global relationList, uidtable
    # 接受用户名
    userName = sock.recv(20)
    # 返回用户id
    uid = uidtable[userName.decode(coding)]
    # 保存客户端信息
    save(sock, uid)

    # 获得 contactName
    contact = sock.recv(20)
    cid = uidtable[contact.decode(coding)]
    # uid=str(cid)
    sock.send(hex(cid))
    
    print('%s 已连接.' % userName)
    return uid


# 处理链接之后事务
def acc(sock):
    
    transmit(sock, init(sock))


def main():
    while True:
        # 链接客户端
        global conList
        client, addr = server.accept()
        # 新建线程 接收信息  发送信息
        a = threading.Thread(target=acc, args=(client,))
        a.start()


if __name__ == '__main__':
    main()

