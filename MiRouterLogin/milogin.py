#!/usr/bin/env python
# coding=utf-8
# code by 92ez.com

import requests
from Crypto.Hash import SHA
import random
import time
import json
import sys
import re

reload(sys)
sys.setdefaultencoding('utf8')


def get_router_token(host):

    home_request = requests.get('http://' + host + '/cgi-bin/luci/web/home')
    key = re.findall(r'key: \'(.*)\',', home_request.text)[0]
    mac = re.findall(r'deviceId = \'(.*)\';', home_request.text)[0]

    aim_url = "http://" + host + "/cgi-bin/luci/api/xqsystem/login"
    nonce = "0_" + mac + "_" + str(int(time.time())) + "_" + str(random.randint(1000, 10000))
    pwd_text = sys.argv[2]

    pwd = SHA.new()
    pwd.update(pwd_text + key)
    hex_pwd_1 = pwd.hexdigest()

    pwd2 = SHA.new()
    pwd2.update(nonce + hex_pwd_1)
    hex_pwd_2 = pwd2.hexdigest()

    data = {
        "logtype": 2,
        "nonce": nonce,
        "password": hex_pwd_2,
        "username": "admin"
    }

    response = requests.post(url=aim_url, data=data, timeout=5)
    result_json = json.loads(response.content)

    if result_json['code'] == 0:
        return result_json['token']
    else:
        return False


def get_router_info(host, token):

    base_url = 'http://' + host + '/cgi-bin/luci/;stok=' + token + '/api/misystem/status'
    wan_url = 'http://' + host + '/cgi-bin/luci/;stok=' + token + '/api/xqnetwork/wan_info'
    stop_url = 'http://' + host + '/cgi-bin/luci/;stok=' + token + '/api/xqnetwork/pppoe_stop'
    start_url = 'http://' + host + '/cgi-bin/luci/;stok=' + token + '/api/xqnetwork/pppoe_start'
    pppoe_url = 'http://' + host + '/cgi-bin/luci/;stok=' + token + '/api/xqnetwork/pppoe_status'
    reboot_url = 'http://' + host + '/cgi-bin/luci/;stok=' + token + '/api/xqnetwork/reboot?client=web'

    getStatus(base_url)
    get_router_wan(wan_url)

    action = sys.argv[3]

    if action == 'reconnect':
        do_reconnect(stop_url, start_url, pppoe_url)
    elif action == 'restart':
        do_reboot(reboot_url)
    else:
        pass


def getStatus(url):
    try:
        router_status = json.loads(requests.get(url, timeout=5).content)

        router_dev = router_status['dev']

        print '[CPU]: ' + str(router_status['cpu']['core']) + '核   ' + router_status['cpu']['hz'] + '   系统负载 ' + str(router_status['cpu']['load'])
        print '[MAC]: ' + router_status['hardware']['mac']
        print '[MEM]: Type: ' + router_status['mem']['type'] + '   Total: ' + router_status['mem']['total'] + '   Usage: ' + str(router_status['mem']['usage']*100) + '% \n'
        print '--------------------[在线设备]----------------------\n'
        for dev in router_dev:
            print dev['mac'] + ' ' + dev['devname']
    except Exception, e:
        print e


def get_router_wan(url):
    try:
        router_wan_info = json.loads(requests.get(url, timeout=5).content)
        print '\n--------------------[外网信息]----------------------\n'
        print '用户: ' + router_wan_info['info']['details']['username']
        print '密码: ' + router_wan_info['info']['details']['password']
        print '类型: ' + router_wan_info['info']['details']['wanType']
        print 'IP地址: ' + router_wan_info['info']['ipv4'][0]['ip']
        print '网关: ' + router_wan_info['info']['gateWay']
        print 'DNS: ' + router_wan_info['info']['dnsAddrs'] + ',' + router_wan_info['info']['dnsAddrs1']
    except Exception, e:
        print e


def do_reconnect(stop, start, pppoe):
    print '\n--------------------[重新拨号]--------------------\n'
    try:
        current_ip = json.loads(requests.get(pppoe, timeout=5).content)['ip']['address']
        if len(current_ip) < 1:
            print '[*] 无法获取到IP地址，网络可能未连接...'
        else:
            print '[*] 当前IP地址：' + current_ip
        stopInfo = json.loads(requests.get(stop, timeout=5).content)
        if stopInfo['code'] == 0:
            print '[*] 等待3秒...'
            time.sleep(3)
            start_info = json.loads(requests.get(start, timeout=5).content)
            if start_info['code'] == 0:
                print '[*] 拨号操作成功！等待运营商返回信息...'
                time.sleep(8)
                router_new_ip = json.loads(requests.get(pppoe, timeout=5).content)['ip']['address']
                if len(router_new_ip) < 1:
                    print '[*] 运营商返回失败，尝试重新拨号...'
                    do_reconnect(stop, start, pppoe)
                else:
                    print '[*] 运营商返回拨号成功，新IP地址：' + router_new_ip
            else:
                print '[*] 出现异常！'
        else:
            print '[*] 出现异常！'
    except Exception, e:
        print '[*] 出现异常！' + str(e)


def do_reboot(url):
    try:
        reboot = json.loads(requests.get(url, timeout=5).content)
        if reboot['code'] == 0:
            print '[*] 正在重启...'
        else:
            print '[*] 重启失败！'
    except Exception, e:
        print e

if __name__ == '__main__':
    print '\n########### Login Mi Router Test Py ############'
    print '		Author 92ez.com'
    print '################################################\n'

    try:
        host = sys.argv[1]
        token = get_router_token(host)

        if token:
            get_router_info(host, token)
        else:
            print '[*] 登录失败！'
    except KeyboardInterrupt:
        print '\n结束进程，程序已退出...'
        sys.exit()
