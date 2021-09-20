#!/usr/bin/python python3
# coding=utf-8
'''
Author: whalefall
Date: 2021-09-20 11:47:04
LastEditTime: 2021-09-20 11:52:59
Description: 蓝本的路由
'''
from . import main
@main.route('/')
def index():
    return 'hello test'
