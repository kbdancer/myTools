#!/usr/bin/env python
# coding=gb2312
# code by 92ez.com

from threading import Thread
import requests
import Queue
import json
import sys
import re

reload(sys)
sys.setdefaultencoding('gb2312')
requests.packages.urllib3.disable_warnings()


def bThread(ip_list):
    thread_list = []
    queue = Queue.Queue()
    hosts = ip_list
    for host in hosts:
        queue.put(host)
    for x in xrange(0, int(sys.argv[1])):
        thread_list.append(tThread(queue))
    for t in thread_list:
        try:
            t.daemon = True
            t.start()
        except:
            pass
    for t in thread_list:
        t.join()


class tThread(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while not self.queue.empty():
            host = self.queue.get()
            do_main_action(host)


def get_ips_by_138(host):
    try:
        ip_url = "http://www.ip138.com/ips1388.asp?ip=" + host + "&action=2"
        header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0"}
        req = requests.get(url=ip_url, headers=header, timeout=10)
        isp_res = re.findall(r'<ul class="ul1">(.+?)</ul>', req.content)[0]
        first_result = re.findall(r'<li>(.+?)</li>', isp_res)[0].split(' ')[-1]
        return unicode(first_result)
    except Exception, e:
        # print e
        pass


def do_main_action(ip_info):
    id = json.loads(ip_info)['id']
    ip = json.loads(ip_info)['ip']
    isp_info = get_ips_by_138(ip)
    try:
        url = 'http://www.abc.com/setisp.php?id=' + str(id) + '&isp=' + isp_info
        set_result = json.loads(requests.get(url).content)
        if set_result['code'] == 0:
            print url + ' -> OK'
        else:
            print url + ' -> error'
    except Exception, e:
        # print e
        pass


def get_no_isp():
    try:
        result = json.loads(requests.get('http://www.abc.com/noisp.php').content)
        bThread(result['data'])
    except Exception, e:
        print e


if __name__ == '__main__':
    get_no_isp()