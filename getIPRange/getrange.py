#!/usr/bin/env python
# coding=utf-8
# code by 92ez.com

from threading import Thread
import requests
import sqlite3
import Queue
import json
import sys
import re

reload(sys)
sys.setdefaultencoding('utf8')

#main function
def bThread(iplist):
    threadl = []
    queue = Queue.Queue()
    hosts = iplist
    for host in hosts:
        queue.put(host)
    for x in xrange(0, 200):
        threadl.append(tThread(queue))
    for t in threadl:
        try:
            t.daemon = True
            t.start()
        except:
            pass
    for t in threadl:
        t.join()

#create thread
class tThread(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while not self.queue.empty():
            host = self.queue.get()
            try:
                saveDetial(host)
            except Exception,e:
                continue

#ip to num
def ip2num(ip):
    ip = [int(x) for x in ip.split('.')]
    return ip[0] << 24 | ip[1] << 16 | ip[2] << 8 | ip[3]

#num to ip
def num2ip(num):
    return '%s.%s.%s.%s' % ((num & 0xff000000) >> 24,(num & 0x00ff0000) >> 16,(num & 0x0000ff00) >> 8,num & 0x000000ff)

#get list
def ip_range(start, end):
    return [num2ip(num) for num in range(ip2num(start), ip2num(end) + 1) if num & 0xff]

def getposition(host):
    print '[*] Get info for '+host
    try:
        ipurl = "http://ip.taobao.com/service/getIpInfo.php?ip="+host
        header = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0"}
        req = requests.get(url = ipurl,headers = header,timeout = 5)
        jsondata = json.loads(req.content.decode('utf8').encode('utf8'))['data']
        info = [jsondata['country'],jsondata['region'],jsondata['city'],jsondata['isp']]
        return info
    except Exception, e:
        getposition(host)

def getData():
    try:
        ipurl = "http://ips.chacuo.net/down/t_txt=p_FJ"
        header = {
            "User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0",
            "Referer":"http://ips.chacuo.net/view/s_FJ",
            "Cookie":"cf_clearance=eec7c0bb365ace6d2d19d154915b460aaf721fcb-1469002765-1800;__cfduid=db929bc6a7fdce16bf7a52c85e0e99aab1468243081; Hm_lvt_ef483ae9c0f4f800aefdf407e35a21b3=1468243072,1468400923,1468590177,1468994895; bdshare_firstime=1468401606542; Hm_lpvt_ef483ae9c0f4f800aefdf407e35a21b3=146899492"
        }
        req = requests.get(url = ipurl,headers = header,timeout = 5)
        resultData = req.content.replace('\t','-').split()[1:-1]
        print '[*] Got data.'
        print '[*] Saving data...'
        saveData(resultData)
    except Exception, e:
        print e

def saveData(items):   
    ipcount = 0
    try:
        cx = sqlite3.connect(sys.path[0]+"/IPRange.db")
        cx.text_factory = str
        cu = cx.cursor()
        cu.execute("delete from ranges")
        cu.execute("update sqlite_sequence SET seq = 0 where name ='ranges'")
        for item in items:
            begin = item.split('-')[0]
            end = item.split('-')[1]
            count = item.split('-')[2]
            ipcount = ipcount + int(count)
            thisList = ip_range(begin,end)
            bThread(thisList)
            cu.execute("insert into ranges (begin,end,count) values (?,?,?)", (begin,end,count))
            cx.commit()
        cu.close()
        cx.close()
        print '[*] Saved.Total '+ str(ipcount)+'.'
    except Exception, e:
        print e

def saveDetial(ip):
    try:
        cx = sqlite3.connect(sys.path[0]+"/IPS.db")
        cx.text_factory = str
        cu = cx.cursor()
        cu.execute("select * from ips where ip='%s'" % (ip))
        if not cu.fetchone():
            posData = getposition(ip)
            country = unicode(posData[0])
            province = unicode(posData[1])
            city = unicode(posData[2])
            isp = unicode(posData[3])
            print '[√] Saving  '+ip
            cu.execute("insert into ips (ip,country,province,city,isp) values (?,?,?,?,?)", (ip,country,province,city,isp))
            cx.commit()
        cu.close()
        cx.close()
    except Exception, e:
        print e

if __name__ == '__main__':
    print '\n############# Get active ip range #############'
    print '                Author 92ez.com'
    print '################################################\n'

    getData()
