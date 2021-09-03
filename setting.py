#!/usr/bin/python python3
# coding=utf-8
'''
Author: whalefall
Date: 2021-08-20 03:03:03
LastEditTime: 2021-09-04 01:46:28
Description: Flask 设置文件
'''
from pathlib import Path
SESSION_TYPE = 'filesystem'  # session 模式
SECRET_KEY = 'lovehyy2021209classpzezprem'  # 密钥
JSON_AS_ASCII = False  # 禁止json中文自动转码
PERMANENT_SESSION_LIFETIME = 10  # session超时时间
PROJECT_PATH = Path(__file__).resolve().parent  # 项目主文件夹

# 下面是 GitHub 配置
UPLOAD_PIC = True  # 是否开启图片上传GitHub
GITHUB_TOKEN = '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'  # GitHub令牌(示例,已取消)
USERNAME = 'AdminWhaleFall'
REPO = 'pic'  # 储存仓库名
REPO_PATH='catch_pic' # 储存仓库路径

# 下面是数据库配置
import os
import sys
WIN = sys.platform.startswith('win')
if WIN:  # 如果是 Windows 系统，使用三个斜线
    prefix = 'sqlite:///'
else:  # 否则使用四个斜线
    prefix = 'sqlite:////'
SQLALCHEMY_DATABASE_URI = prefix + os.path.join(PROJECT_PATH, 'db','log.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False  # 关闭对模型修改的监控