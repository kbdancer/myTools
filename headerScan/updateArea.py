#!/usr/bin/env python
# coding=gb2312
# code by 92ez.com

from threading import Thread
import requests
import Queue
import json
import sys

reload(sys)
sys.setdefaultencoding('gb2312')


def bThread(iplist):
    thread_list = []
    queue = Queue.Queue()
    hosts = iplist
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


def get_location_by_taobao(host):
    try:
        ip_url = "http://ip.taobao.com/service/getip_info.php?ip=" + host
        header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0"}
        req = requests.get(url=ip_url, headers=header, timeout=10)
        json_data = json.loads(req.content.decode('utf8').encode('utf8'))['data']
        info = [json_data['country'], json_data['region'], json_data['city'], json_data['isp']]
        return info
    except Exception, e:
        # print e
        pass


def get_no_area():
    try:
        result = json.loads(requests.get('http://www.abc.com/noarea.php').content)
        bThread(result['data'])
    except Exception, e:
        print e


def do_main_action(ip_info):
    id = json.loads(ip_info)['id']
    ip = json.loads(ip_info)['ip']
    location_string = get_location_by_taobao(ip)
    try:
        url = 'http://www.abc.com/setarea.php?id=' + str(id) + '&country=' + location_string[0] + '&province=' + location_string[1] + '&city=' + location_string[2]
        set_result = json.loads(requests.get(url).content)
        if set_result['code'] == 0:
            print url + ' -> OK'
        else:
            print url + ' -> error'
    except Exception, e:
        # print e
        pass

if __name__ == '__main__':
    get_no_area()