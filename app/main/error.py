#!/usr/bin/python python3
# coding=utf-8
'''
Author: whalefall
Date: 2021-09-20 11:47:18
LastEditTime: 2021-09-20 11:50:57
Description: 主蓝本的错误处理
'''
from flask import render_template
from . import main
from flask import redirect


@main.app_errorhandler(404)
def page_not_found(e):
    """注册应用全局错误处理"""
    return e, 404


@main.app_errorhandler(401)
def authfail(e):
    return redirect('/static/401.jpg')
