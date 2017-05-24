#!/usr/bin/env python
# coding=utf-8
# code by kbdancer@92ez.com

import threading
import requests
import Queue
import json
import sys
import re
import os

reload(sys)
sys.setdefaultencoding('utf8')


def ip2num(ip):
    ip = [int(x) for x in ip.split('.')]
    return ip[0] << 24 | ip[1] << 16 | ip[2] << 8 | ip[3]


def num2ip(num):
    return '%s.%s.%s.%s' % ((num & 0xff000000) >> 24, (num & 0x00ff0000) >> 16, (num & 0x0000ff00) >> 8, num & 0x000000ff)


def ip_range(start, end):
    return [num2ip(num) for num in range(ip2num(start), ip2num(end) + 1) if num & 0xff]


def bThread(ip_list):
    thread_list = []
    queue = Queue.Queue()
    for host in ip_list:
        queue.put(host)

    for x in xrange(0, int(SETTHREAD)):
        thread_list.append(tThread(queue))

    for t in thread_list:
        t.start()
    for t in thread_list:
        t.join()


class tThread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while not self.queue.empty():
            host = self.queue.get()
            check_serve_info(host)


def get_ports_from_remote():
    tmp_port = []
    try:
        ports_result = json.loads(
            requests.get(url='http://header.telnetscan.org/app/ports.php', headers=HEADERS, timeout=15).content)
        for port in ports_result['data']:
            tmp_port.append(int(port))
        return tmp_port
    except Exception, e:
        print e


def check_serve_info(host):
    for k in PORTS:
        try:
            aim_url = "http://" + host + ":" + str(k)
            response = requests.get(url=aim_url, headers=HEADERS, timeout=5)
            for header_item in response.headers:
                if 'erver' in header_item:
                    server_text = response.headers[header_item]
            title_text = re.findall(r'<title>(.*?)</title>', response.content.decode('utf-8').encode('utf-8'))[0]

            if len(server_text) > 0:
                save_data = {"ip": host, "port": str(k), "server": server_text, "title": title_text}
                print str(save_data)
                save_data_to_server(save_data)
        except Exception, e:
            # print e
            pass


def save_data_to_server(aim_data):
    try:
        result = json.loads(
            requests.post(url='http://header.telnetscan.org/app/insertto.php', headers=HEADERS, data=aim_data, timeout=15).content)

        if result['code'] == 0:
            print "Save Success!"
        else:
            print "Save Failed!"

    except Exception, e:
        print e


if __name__ == '__main__':
    print '############# HTTP Header Scanner ###########'
    print '                Author 92ez.com'
    print '#############################################\n'

    global SETTHREAD
    global this_pid
    global PORTS
    global HEADERS

    HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0"}

    this_pid = os.getpid()
    PORTS = get_ports_from_remote()
    print '[*] This pid is ' + str(this_pid)

    try:
        SETTHREAD = sys.argv[1]
        startIp = sys.argv[2].split('-')[0]
        endIp = sys.argv[2].split('-')[1]
        ip_list = ip_range(startIp, endIp)
        print '[Note] Will scan ' + str(len(ip_list)) + " host...\n"
        bThread(ip_list)
    except KeyboardInterrupt:
        print '\n[*] Kill all thread.'
        os.kill(this_pid, 9)
