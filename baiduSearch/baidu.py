#!/usr/bin/env python3
# coding=utf-8
# code by 92ez.com

import requests
import sys
import re


def get_urls(keyword, page_count):
    titles = []
    old_links = []
    custom_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0"}
    try:
        for page in range(0, page_count):
            this_page_url = "https://www.baidu.com/s?wd=" + keyword + '&pn=' + str(page * 10)
            print(this_page_url)
            html_page = requests.get(url=this_page_url, headers=custom_headers).content.decode('utf8')
            filter_string = html_page.replace('\n', '').replace('\t', '')
            title_str = re.findall(r'<h3 class="t">(.*?)</h3>', filter_string)

            for tit in title_str:
                try:
                    tmp_string = tit.replace('<em>', '').replace('</em>', '').replace(' ', '')
                    this_title = re.findall(r'blank\">(.+?)</a>', tmp_string)[0]
                    this_old_link = re.findall(r'href=\"(.+?)"target', tmp_string)[0]
                    titles.append(this_title)
                    old_links.append(this_old_link)
                except:
                    pass
        return titles, old_links
    except Exception as e:
        print(e)


if __name__ == '__main__':

    keywords = sys.argv[2]
    max_page = int(sys.argv[1])
    real_domains = []
    real_links = []

    print('[*] 当前设置获取前' + str(max_page * 10) + '个结果')
    print('[*] 获取结果页标题和百度原始链接...')
    titleArr, oldinkArr = get_urls(keywords, max_page)
    print('[√] 获取到' + str(len(titleArr)) + '个标题和原始链接')

    print('[*] 开始提取真实链接...')
    for link in oldinkArr:
        this_header = requests.head(link).headers
        this_domain = this_header['Location'].split('://')[1].split('/')[0]
        this_real_url = this_header['Location'].split('://')[0] + '://' + this_header['Location'].split('://')[1]
        real_domains.append(this_domain)
        real_links.append(this_real_url)
        print('[*] 域名:' + this_domain + ' --> ' + this_real_url)
    print('[√] 提取真实链接完成')
    # 写入真实链接到文本
    real_links = set(real_links)
    with open(sys.path[0] + '/search_link.txt', 'wb') as f:
        for host in real_links:
            f.write(str.encode(host+'\n'))
    # 写入域名到文本
    real_domains = set(real_domains)
    with open(sys.path[0] + '/search_domains.txt', 'wb') as f:
        for host in real_domains:
            f.write(str.encode(host+'\n'))
