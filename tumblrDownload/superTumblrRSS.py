#!/usr/bin/env python
# coding=utf-8

import threading
import requests
import queue
import sys
import os
import re


def MyThread(bloglist):
    threads = []
    queue_list = queue.Queue()
    for user in bloglist:
        queue_list.put(user)

    for x in range(0, int(SETTHREAD)):
        threads.append(tThread(queue_list))

    for t in threads:
        t.start()
    for t in threads:
        t.join()


class tThread(threading.Thread):
    def __init__(self, queue_list):
        threading.Thread.__init__(self)
        self.queue_list = queue_list

    def run(self):
        while not self.queue_list.empty():
            blog_url = self.queue_list.get()
            try:
                get_source(blog_url)
            except:
                continue


def get_source(blog_url):
    if "/rss" not in blog_url:
        blog_url += "rss"
    print('[o] Get source from blog %s ...' % blog_url)
    try:
        response_string = requests.get(url=blog_url, timeout=50).content.decode('utf8').replace('\n', '')
        source_image_list = re.findall(r'img src="(.+?)"', response_string)
        source_video_list = re.findall(r'source src="(.+?)"', response_string)
        if len(source_image_list) > 0 or len(source_video_list) > 0:
            blog_dir = sys.path[0] + '/RSSdownload/' + re.findall(r'//(.+?)/', blog_url)[0] + '/'
            if not os.path.exists(blog_dir):
                os.makedirs(blog_dir)
            if len(source_image_list) > 0:
                img_dir = blog_dir + 'image/'
                if not os.path.exists(img_dir):
                    os.makedirs(img_dir)
                for source in source_image_list:
                    if 'media.tumblr.com' in source:
                        # pass
                        write_file(source, img_dir, source.split('/')[-1])
            if len(source_video_list) > 0:
                video_dir = blog_dir + 'video/'
                if not os.path.exists(video_dir):
                    os.makedirs(video_dir)
                for source in source_video_list:
                    # print(source)
                    write_file(source, video_dir, source.split('/')[-1] + '.mp4')
    except Exception as e:
        print(e)


def write_file(source_url, dir_path, file_name):
    if not os.path.exists(dir_path + file_name):
        print('[*] Source %s is downloading...' % file_name)
        file_download = requests.get(url=source_url, timeout=50)
        if file_download.status_code == 200:
            open(dir_path + file_name, 'wb').write(file_download.content)
    else:
        print('[*] Source %s has been downloaded.' % file_name)


def get_rss_blog():
    rss_url = "https://pastebin.com/raw/zmKcfPqg"
    try:
        rss_response = requests.get(url=rss_url, timeout=20).content.decode('utf8')
        xml_url = re.findall(r'xmlUrl="(.+?)"', rss_response)
        MyThread(xml_url)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    global SETTHREAD
    SETTHREAD = 10
    get_rss_blog()
