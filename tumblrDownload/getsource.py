#!/usr/bin/env python
# coding=utf-8

import requests
import sys
import os
import re


def get_source(nickname, page_index, source_type):
    aim_url = "https://%s.tumblr.com/page/%d" % (nickname, page_index)
    print('[o] Get source from blog %s ...' % aim_url)
    try:
        response_string = requests.get(url=aim_url, timeout=50).content.decode('utf8').replace('\n', '')
        if "posts-no-posts content" not in response_string:
            if source_type == "images":
                source_elements = re.findall(r'<img(.+?)>', response_string)
                source_iframes = re.findall(r'id="photoset_iframe(.+?)>', response_string)  # for special images iframe
                if len(source_iframes) > 0:
                    for iframe_item in source_iframes:
                        this_iframe_url = re.findall(r'src="(.+?)"', iframe_item)[0]
                        image_iframe_url = "https://%s.tumblr.com" % nickname + this_iframe_url
                        images_iframe_response = requests.get(url=image_iframe_url, timeout=50).content.decode('utf8').replace('\n', '')
                        iframe_images = re.findall(r'<img(.+?)>', images_iframe_response)
                        source_elements += iframe_images
            else:
                source_elements = re.findall(r'<iframe(.+?)>', response_string)

            if len(source_elements) > 0:
                dir_path = sys.path[0] + '/' + aim_url.split('//')[1].split('.')[0] + '/'
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)

                for this_source in source_elements:
                    if source_type == "images":
                        img_dir = dir_path + 'image/'
                        if not os.path.exists(img_dir):
                            os.makedirs(img_dir)
                        image_url = re.findall(r'src="(.+?)"', this_source)[0]
                        image_name = image_url.split('/')[-1]
                        if "tumblr_" in image_name:
                            write_file(image_url, img_dir, image_name)
                    else:
                        if "/video/" in this_source:
                            video_dir = dir_path + 'video/'
                            if not os.path.exists(video_dir):
                                os.makedirs(video_dir)
                            video_url = re.findall(r"src='(.+?)'", this_source)[0]
                            video_response = requests.get(url=video_url, timeout=50).content.decode('utf8').replace('\n', '')
                            video_source = re.findall(r'<source src="(.+?)"', video_response)[0]
                            video_name = video_source.split('/')[-1] + '.mp4'
                            write_file(video_source, video_dir, video_name)

            else:
                print('[x] Can not get any source.')
            page_index += 1
            get_source(nickname, page_index, source_type)
        else:
            print('[!] Get source complete!')
    except Exception as e:
        print(e)
        get_source(nickname, page_index, source_type)


def write_file(source_url, dir_path, file_name):
    if not os.path.exists(dir_path + file_name):
        print('[*] Source %s is downloading...' % file_name)
        file_download = requests.get(url=source_url, timeout=50)
        if file_download.status_code == 200:
            open(dir_path + file_name, 'wb').write(file_download.content)
    else:
        print('[*] Source %s has been downloaded.' % file_name)


if __name__ == '__main__':
    source_type = sys.argv[1]
    # source_type = "images"
    user_nickname = sys.argv[2]
    # user_nickname = "itunesartworks"
    get_source(user_nickname, 1, source_type)
