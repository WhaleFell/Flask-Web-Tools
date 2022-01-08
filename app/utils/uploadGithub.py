#!/usr/bin/python python3
# coding=utf-8
"""
Author: WhaleFall
Date: 2021-08-23 01:05:26
LastEditTime: 2021-08-26 18:22:56
Description: 上传抓拍到的文件到GitHub
"""
import re
# import requests
import base64
import json
# from flask import current_app  # 应用上下文对象
import time
from pathlib import Path
import os
import sys
# 上层路径导入
sys.path.append("..")


# # 将文件转换为base64编码，上传文件必须将文件以base64格式上传
def file2base64(path):
    '''传入文件路径'''
    print(path)
    with open(path, "rb") as p:
        data = p.read()
    data_b64 = base64.b64encode(data).decode('utf-8')
    return data_b64


# def upload_catch_pic(path_pic, file_name=int(time.time())):
#     '''传入图片base64后的数据,保存到GitHub,新建线程挂后台执行'''
#     # 获取配置信息并判断
#     token = setting.GITHUB_TOKEN
#     able = setting.UPLOAD_PIC
#     repo = setting.REPO
#     username = setting.USERNAME
#     path = setting.REPO_PATH
#
#     if not able:
#         print("禁止上传文件!")
#         return
#
#     # 用户名、库名、路径
#     url = f"https://api.github.com/repos/{username}/{repo}/contents/{path}/{file_name}.jpg"
#     headers = {"Authorization": "token " + token}
#     content = file2base64(path_pic)
#     data = {
#         "message": "message",
#         "committer": {
#             "name": "AdminWhaleFall",
#             "email": "2734184475@qq.com"
#         },
#         "content": content
#     }
#     try:
#         data = json.dumps(data)
#         req = requests.put(url=url, data=data, headers=headers)
#         req.encoding = "utf-8"
#         re_data = json.loads(req.text)
#         print(re_data)
#         # print(re_data['content']['sha'])
#         # print("https://cdn.jsdelivr.net/gh/[user]/[repo]/[path]"+file_name)
#         return re_data
#     except Exception as e:
#         print("图片上传时发生错误,", e)
#         return False


def save_base64_pic(base64_pic,file_name=int(time.time())):
    '''保存base64图片'''
    if base64_pic:
        
        pic_path = Path(__file__).resolve(
        ).parent.parent.joinpath('static', 'catch')
        pic_path.mkdir(exist_ok=True)
        pic_path = pic_path.joinpath('%s.jpg' % (file_name))
        with open(pic_path, "wb") as p:
            p.write(base64.b64decode(base64_pic))

        return True
       
    return False


if __name__ == '__main__':
    # fdata = open_file('cloud.jpg')
    # upload_file(fdata)
    pass
