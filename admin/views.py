#!/usr/bin/python python3
# coding=utf-8
'''
Author: whalefall
Date: 2021-08-26 17:16:53
LastEditTime: 2021-08-26 17:22:32
Description: 蓝图文件
'''
import os
import sys
sys.path.append(os.getcwd())

from flask import request, current_app, session, render_template, make_response, Response, abort
from flask import *

from . import admin

@admin.route('/admin/',methods=['GET','POST'])
def admin_index():
    return 'ADMIN'

