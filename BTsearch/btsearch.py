#!/usr/bin/env python
# coding=utf-8
# code by kbdancer@92ez.com

import threading
import requests
import sqlite3
import Queue
import json
import sys
import re

reload(sys)
sys.setdefaultencoding('utf8')


W = '\033[0m'  # white (normal)
R = '\033[31m'  # red
G = '\033[32m'  # green


def bThread(url_list):
    threadl = []
    queue = Queue.Queue()
    for url in url_list:
        queue.put(url)

    for x in xrange(0, 20):
        threadl.append(tThread(queue))

    for t in threadl:
        t.start()
    for t in threadl:
        t.join()


class tThread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):

        while not self.queue.empty():
            url = self.queue.get()
            try:
                decode_btant(url)
            except:
                continue


def get_url_by_btant():
    keyword = sys.argv[1]
    url = "http://www.btany.com/search/" + keyword + "-first-asc-1"
    print '[*] 获取 www.btany.com 基本信息...'
    try:
        response_string = requests.get(url=url, verify=False, HEADERS=HEADERS, timeout=20).content
        # no result
        if len(response_string.split('<span>无<b>')) > 1:
            return json.dumps({"code": -1, "msg": "can not find any page!"})
            sys.exit()

        temp_page = re.findall(r'<div class="bottom-pager">(.+?)</div>', response_string, re.S)[0].replace('\n', '')
        page_string = re.findall(r'<a href="(.+?)">', temp_page)

        if len(page_string) < 1:
            # only one page
            max_page_number = 1
        else:
            max_page_number = int(re.findall(r'<a href="(.+?)">', temp_page)[-1].split('asc-')[1])

        url_list = []

        for pl in range(1, max_page_number + 1):
            url_list.append("http://www.btany.com/search/" + keyword + "-first-asc-" + str(pl))

        bThread(url_list)

    except Exception, e:
        print e


def decode_btant(url):
    print '[*] 正在解析 '+ url + ' 的数据...'
    try:
        decode_html = requests.get(url=url, HEADERS=HEADERS, verify=False, timeout=20).content

        magnet = re.findall(r'href="magnet(.+?)"', decode_html)
        thunder = re.findall(r'href="thunder(.+?)"', decode_html)
        title = re.findall(r'<div class="item-list">(.+?)</div>', decode_html, re.S)

        for x in range(0, len(magnet)):
            temp_title = title[x].replace('<span class="highlight">', '').replace('</span>', '').replace('\n', ' ')
            size = re.findall(r'<span>(.+?)</p>', temp_title)
            title_text = re.findall(r'<p>(.+?)<span>', temp_title)

            # to fix some ad script
            trash_code = re.findall(r'<a(.+?)script>', title_text[0])

            if len(trash_code) > 0:
                trash_title = title_text[0]
                for t in range(0, len(trash_code)):
                    trash_title = trash_title.replace('<a' + trash_code[t] + 'script>', "")
                real_title = trash_title
            else:
                real_title = title_text[0]

            result_data = {"title": real_title, "magnet": "magnet" + magnet[x], "thunder": "thunder" + thunder[x], "size": size[0]}
            QUERY_LIST.append(result_data)
    except Exception, e:
        print e


def clear_data():
    print '[*] 清空上一次的采集数据...'
    try:
        cx = sqlite3.connect(sys.path[0] + "/search.db")
        cx.text_factory = str
        cu = cx.cursor()
        cu.execute("delete from `record`")
        cu.execute("update sqlite_sequence SET seq = 0 where name ='record'")
        cx.commit()
        cu.close()
        cx.close()
    except Exception, e:
        print e


def save_data():
    print '[*] 开始存储数据到数据库...'
    save_count = 0
    try:
        cx = sqlite3.connect(sys.path[0] + "/search.db")
        cx.text_factory = str
        cu = cx.cursor()
        print len(QUERY_LIST)
        for m in QUERY_LIST:
            cu.execute("select * from record where magnet=? or thunder=?", (m['magnet'], m['thunder']))
            if not cu.fetchone():
                cu.execute("insert into record (title,magnet,thunder,size) values (?,?,?,?)", (m['title'], m['magnet'], m['thunder'], m['size']))
                cx.commit()
                print '[√] => Insert successly!'
                save_count = save_count + 1
            else:
                print R + '[x] <= Found in database!' + W
        cu.close()
        cx.close()

        print '*' * 60
        print '[√] 数据采集完成，共采集%s条' % str(len(QUERY_LIST))
        print '[√] 数据存储完成，共存储%s条' % save_count
    except Exception, e:
        print e


if __name__ == '__main__':
    global QUERY_LIST
    global HEADERS

    QUERY_LIST = []
    HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0"}

    print '[*] Searching ...'
    print '[*]' + '-' * 60

    get_url_by_btant()
    clear_data()
    save_data()