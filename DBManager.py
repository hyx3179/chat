#!/usr/bin/python3
# -*- coding:utf-8 -*-

import pymysql


# 链接数据库并执行语句 setence
def link(setence):
    db = pymysql.connect('localhost','root','7890','chat' )
    cursor = db.cursor()
    result = cursor.execute(setence)
    db.commit()
    db.close()
    return result


# 新建用户信息表
def createTableUserInfo():
    setence = ''' create table userInfo (
                uId int auto_increment,
                uName char(20),
                passwd char(32),
                primary key(uId)
                )'''
    link(setence)


# 新建用户表
def createTable(userName):
    setence = ''' create table %s (
                contact char(20),
                remarks char(20)
                )''' % userName
    link(setence)


# 查询全部
def select(table):
    setence = 'select * from %s' % table
    db = pymysql.connect('localhost','root','7890','chat' )
    cursor = db.cursor()
    cursor.execute(setence)
    results = cursor.fetchall()
    for row in results:
        print (row)
    # 关闭数据库连接
    db.close()


# 按uId查询
def selectById(table, uId):
    setence = "select * from %s where uId=%s" % (table, uId)
    db = pymysql.connect('localhost','root','7890','chat' )
    cursor = db.cursor()
    result = cursor.execute(setence)
    data = cursor.fetchone()
    db.close()
    return (result, data)


# 按用户名查询
def selectuName(table, uName):
    setence = "select * from %s where uName='%s'" % (table, uName)
    db = pymysql.connect('localhost','root','7890','chat' )
    cursor = db.cursor()
    result = cursor.execute(setence)
    data = cursor.fetchone()
    db.close()
    return (result,data)


# 按用户名查询是否存在
def existent(uName):
    result = selectuName('userInfo', uName)[0]
    if result != 0:
        return True
    return False



# 插入新的列
def insertColumn(table, newColumn, columnType):
    setence = "alter table %s add %s %s" % (table, newColumn, columnType)
    link(setence)


# 插入信息
def insert(table, uName, passwd):
    setence = "insert into %s values(default, '%s', '%s')" % (table, uName, passwd)
    link(setence)


# 根据 uid 删除
def delete(table, uid):
    setence = 'delete from %s where uId=%s' % (table, uid)
    link(setence)


# 匹配用户名和密码
def match(userName, passwd):
    result=selectuName('userInfo', userName)
    if passwd == result[1][2]:
        return True
    else:
        return False


def main():
#    createTableUserInfo()
    # print(existent('userInfo'))
    # print(selectuName('userInfo','zys'))
    # t = selectById('userInfo',1)
    # print(type(t[1][2]))
    # r=selectuName('userInfo','zys')
    # print(r[1][2])
    select('userInfo')
    pass


if __name__ == '__main__':
    main()
