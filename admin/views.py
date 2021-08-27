#!/usr/bin/python python3
# coding=utf-8
'''
Author: whalefall
Date: 2021-08-26 17:16:53
LastEditTime: 2021-08-27 12:30:10
Description: 蓝图文件
'''

from . import admin
from flask import *
from flask import request, current_app, session, render_template, make_response, Response, abort
from utils.write_log import Sql_log
import os
import sys
sys.path.append('..')

def dontreturn(func):
    '''函数如果错误就返回501'''
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            abort(501)
    return inner

def request_parse(req_data) -> dict:
    '''解析请求数据并以字典的形式返回'''
    if req_data.method == 'POST':
        data = req_data.form

    elif req_data.method == 'GET':
        data = req_data.args

    return dict(data)


@admin.route('/admin/', methods=['GET', 'POST'])
def admin_index():
    return render_template('admin_login.html')


@admin.route('/admin/log/', methods=['GET'])
def admin_log():
    return render_template('admin_log.html')


@admin.route('/admin/log/pageLoadJson/', methods=['GET', 'POST'])
@dontreturn
def pageLoad():
    '''提供数据查询分页支持
    前端将传入:  {'pageNumber': '1'当前页码, 'pageSize': '20'每页数量}
    '''
    log = Sql_log()
    req = request_parse(request)
    pageSize = int(req['pageSize'])
    pageNumber = int(req['pageNumber'])
    count = log.count()  # 总数据条数

    r = log.search((pageNumber-1)*pageSize, pageSize)
    pagedata = {
        "pageSize": pageSize,
        "pageNumber": pageNumber,
        "totalRow": count,
        "totalPage": int(count/pageSize),
        "list": [
            res.dict()
            for res in r
        ],
    }
    return jsonify(pagedata)
