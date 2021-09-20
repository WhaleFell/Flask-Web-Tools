#!/usr/bin/python python3
# coding=utf-8
'''
Author: whalefall
Date: 2021-09-20 11:45:08
LastEditTime: 2021-09-20 11:48:02
Description: 主蓝本
蓝本只有注册到应用中才能使用
'''
from flask import Blueprint

# 蓝本的名称和所在的包和模块
main = Blueprint('main',__name__)

# 从当前包引入蓝本视图
from . import error,views