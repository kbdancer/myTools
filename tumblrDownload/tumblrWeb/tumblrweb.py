#!/usr/bin/env python
# coding=utf-8
# author 92ez.com

from flask import Flask, render_template, request, abort, send_from_directory
import requests
import sys
import os
import re

app = Flask(__name__)


@app.route("/search", methods=['POST'])
def search():
    nickname = request.form.get('nickname')
    source_type = request.form.get('type')
    user_id = request.form.get('uid')
    if user_id != "userid123":
        return "can not use!"
    else:
        if len(nickname) > 0:
            get_source(nickname, 1, source_type, user_id)
            return "complete!"
        else:
            return "nickname is empty"


@app.route("/history", methods=['GET'])
def history():
    user_id = request.args.get('uid')
    if len(user_id) < 1:
        return "user id is empty !"
    else:
        try:
            list_data = os.listdir(sys.path[0] + '/download/' + user_id)
            return render_template("history.html", uid=user_id, data=list_data)
        except Exception as e:
            return "user is not exist!"


@app.route("/type", methods=['GET'])
def gettype():
    user_id = request.args.get('uid')
    blog = request.args.get('blog')
    if len(user_id) < 1:
        return "user id is empty !"
    else:
        try:
            list_data = os.listdir(sys.path[0] + '/download/' + user_id + '/' + blog)
            return render_template("type.html", blog=blog, uid=user_id, data=list_data)
        except Exception as e:
            return "user is not exist!"


@app.route("/list", methods=['GET'])
def getlist():
    user_id = request.args.get('uid')
    blog = request.args.get('blog')
    dir = request.args.get('dir')
    if len(user_id) < 1:
        return "user id is empty !"
    else:
        try:
            list_data = os.listdir(sys.path[0] + '/download/' + user_id + '/' + blog + '/' + dir)
            return render_template("list.html", blog=blog, type=dir, uid=user_id, data=list_data)
        except Exception as e:
            return "user is not exist!"


@app.route("/download", methods=['GET'])
def download():
    filepath = sys.path[0] + '/download/' + request.args.get('path')
    filename = request.args.get('name')
    if os.path.isfile(filepath + filename):
        print(filepath + filename)
        return send_from_directory(filepath, filename, as_attachment=True)
    else:
        abort(404)


@app.route("/")
def index():
    return render_template("index.html")


def get_source(nickname, page_index, source_type, user_id):
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
                dir_path = sys.path[0] + '/download/' + user_id + '/' + aim_url.split('//')[1].split('.')[0] + '/'
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


if __name__ == "__main__":
    app.run(debug=True)