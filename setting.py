#!/usr/bin/python python3
# coding=utf-8
'''
Author: whalefall
Date: 2021-08-20 03:03:03
LastEditTime: 2021-08-20 09:57:51
Description: Flask 设置文件
'''
from pathlib import Path
SESSION_TYPE = 'filesystem'
SECRET_KEY = 'lovehyy2021209classpzezprem'
JSON_AS_ASCII = False
PERMANENT_SESSION_LIFETIME = 10
PROJECT_PATH = Path(__file__).resolve().parent
