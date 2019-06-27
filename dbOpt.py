#!/usr/bin/python3
# -*- coding:utf-8 -*-

import pymysql

# 新建用户信息表
def createTableUserInfo():
    setence = ''' create table userInfo (
                uId int auto_increment,
                uName char(20),
                passwd char(20),
                primary key(uId)
                )'''
    db = pymysql.connect('localhost','root','7890','chat' )
    cursor = db.cursor()
    cursor.execute(setence)
    db.close()


# 新建用户表
def createTable(userName):
    setence = ''' create table %s (
                contact char(20),
                remarks char(20)
                )''' % userName
    db = pymysql.connect('localhost','root','7890','chat' )
    cursor = db.cursor()
    cursor.execute(setence)
    db.close()


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
def selectUseId(table, uid):
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
    return result


# 插入新的列
def insertColumn(table, newColumn, columnType):
    setence = "alter table %s add %s %s" % (table, newColumn, columnType)
    db = pymysql.connect('localhost','root','7890','chat' )
    cursor = db.cursor()
    cursor.execute(setence)
    db.commit()
    db.close()


# 插入信息
def insert(table, uName, passwd):
    setence = "insert into %s values(default, '%s', '%s')" % (table, uName, passwd)
    db = pymysql.connect('localhost','root','7890','chat' )
    cursor = db.cursor()
    cursor.execute(setence)
    db.commit()
    db.close()


# 删除
def delete(table, uid):
    setence = 'delete from %s where uId=%s' % (table, uid)
    db = pymysql.connect('localhost','root','7890','chat' )
    cursor = db.cursor()
    cursor.execute(setence)
    db.commit()
    db.close()


def main():
    createTableUserInfo()
    pass


if __name__ == '__main__':
    main()
