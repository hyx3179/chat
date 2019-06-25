
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
def getUid(message):
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
def transmit(sock, myId):
    while True:
        data = sock.recv(1024)
        if not data:
            break
        ## 拆包 找到 朋友 的 sock
        conTuple[relationList[getUid(data.decode(coding))]].send(data)
        
    sock.close()
    print('%s 断开链接' % myId)
        


def init(sock):
    global relationList, uidtable
    # 接受用户名
    userName = sock.recv(20)
    # 返回用户id
    clientId = uidtable[userName.decode(coding)]
    uid=str(clientId)
    sock.send(uid.encode(coding))
    # 获得friendName
    contact = sock.recv(20)
    # id对应关系表
    relationList[int(uid)]=uidtable[contact.decode(coding)]
    # 保存客户端信息
    save(sock, clientId)
    print('%s 已连接.' % userName)
    return clientId


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

