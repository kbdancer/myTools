#!/usr/bin/env python
# coding=utf-8
# kbdancer@92ez.com

import MySQLdb
import sys

reload(sys)
sys.setdefaultencoding('utf8')


def save_data_to_mysql(mysql_object, ip_line):
    try:
        begin = ip_line[0:16].replace(' ', '')
        end = ip_line[16:32].replace(' ', '')
        try:
            location = line[32:].split(' ')[0]
        except:
            location = ''
        try:
            isp_type = line[32:].replace('  ', ' ').split(' ')[1].replace('\n', '').replace('\r', '')
        except:
            isp_type = ''

        this_line_value = [begin + "-" + end, location, isp_type]
        do_insert(mysql_object, this_line_value)
    except Exception, e:
        print e


def do_insert(mysql_object, row_data):
    try:
        insert_sql = """INSERT INTO `ipdb` (`iprange`,`location`, `type`) VALUES ( %s, %s, %s )"""
        mysql_object.insert(insert_sql, row_data)
    except Exception, e:
        print row_data
        print e


class Database:
    host = 'localhost'
    user = 'ipdb'
    password = '3u9whrpcEUBTnNNn'
    db = 'ipinfo'
    charset = 'utf8'

    def __init__(self):
        self.connection = MySQLdb.connect(self.host, self.user, self.password, self.db, charset=self.charset)
        self.cursor = self.connection.cursor()

    def insert(self, query, params):
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
        except Exception, e:
            print e
            self.connection.rollback()

    def query(self, query, params):
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, params)
        return cursor.fetchall()

    def __del__(self):
        self.connection.close()


if __name__ == '__main__':
    mysql = Database()
    ip_file = open(sys.path[0] + "/ip.txt")
    print 'Start save to mysql ...'
    for line in ip_file:
        save_data_to_mysql(mysql, line)
    ip_file.close()
    print 'Save complete.'
