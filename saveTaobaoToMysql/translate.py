#!/usr/bin/env python
# coding=utf-8
# code by kbdancer@92ez.com

import MySQLdb
import xlrd
import sys

reload(sys)
sys.setdefaultencoding('utf8')


class Database:
    host = '127.0.0.01'
    user = 'taobao'
    password = 'jDXfZrqki1Fe0XFy'
    db = 'taobao'
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


def do_query(mysql, sql, param):
    try:
        return mysql.query(sql, param)
    except Exception, e:
        print e


def do_insert(mysql, sql, param):
    try:
        mysql.insert(sql, param)
    except Exception, e:
        print e

if __name__ == '__main__':

    mysql = Database()

    data = xlrd.open_workbook(sys.path[0] + '/taobao.xls')
    table = data.sheets()[0]
    count_row = table.nrows

    for x in range(1, count_row):
        this_row_data = table.row_values(x)

        goods_id = this_row_data[0]
        goods_name = this_row_data[1]
        goods_main_pic = this_row_data[2]
        goods_detail_url = this_row_data[3]
        goods_category = this_row_data[4]
        goods_union_url = this_row_data[5]
        goods_price = this_row_data[6]
        goods_sale_count = this_row_data[7]
        goods_adorn_percent = this_row_data[8]
        goods_adorn = this_row_data[9]
        shop_name = this_row_data[12]
        shop_type = this_row_data[13]
        coupon_id = this_row_data[14]
        coupon_count = this_row_data[15]
        coupon_left = this_row_data[16]
        coupon_value = this_row_data[17]
        coupon_begin = this_row_data[18]
        coupon_end = this_row_data[19]
        coupon_url = this_row_data[20]
        coupon_goods_url = this_row_data[21]

        goods_category_id = 0

        temp_cate = ''

        for cate in goods_category.split('/'):
            if temp_cate == '':
                query_res = do_query(mysql, 'SELECT id FROM `category` where cname=%s', [cate])
                if not query_res:
                    do_insert(mysql, 'insert into `category`(cname,parent_id) values(%s,%s)', [cate, '0'])
            else:
                query_son = do_query(mysql, 'SELECT id FROM `category` where cname=%s', [cate])
                if not query_son:
                    father_id = do_query(mysql, 'select id from `category` where cname=%s', [temp_cate])[0]['id']
                    do_insert(mysql, 'insert into `category`(cname,parent_id) values(%s,%s)', [cate, str(father_id)])

            temp_cate = cate

        this_category = do_query(mysql, 'SELECT id,parent_id FROM `category` where cname=%s', [goods_category.split('/')[-1]])

        if this_category[0]['parent_id'] == 0:
            goods_category_id = this_category[0]['id']
        else:
            goods_category_id = this_category[0]['parent_id']

        insert_sql = """
          insert into `goods`(
            goods_id,
            goods_name,
            goods_main_pic,
            goods_detail_url,
            goods_category_id,
            goods_union_url,
            goods_price,
            goods_sale_count,
            goods_adorn_percent,
            goods_adorn,
            shop_name,
            shop_type,
            coupon_id,
            coupon_count,
            coupon_left,
            coupon_value,
            coupon_begin,
            coupon_end,
            coupon_url,
            coupon_goods_url
            ) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """

        params = [
            goods_id,
            goods_name,
            goods_main_pic,
            goods_detail_url,
            goods_category_id,
            goods_union_url,
            goods_price,
            goods_sale_count,
            goods_adorn_percent,
            goods_adorn,
            shop_name,
            shop_type,
            coupon_id,
            coupon_count,
            coupon_left,
            coupon_value,
            coupon_begin,
            coupon_end,
            coupon_url,
            coupon_goods_url
        ]

        do_insert(mysql, insert_sql, params)

