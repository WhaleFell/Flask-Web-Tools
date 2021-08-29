#!/usr/bin/python python3
# coding=utf-8
'''
Author: whalefall
Date: 2021-08-26 17:16:53
LastEditTime: 2021-08-29 11:04:13
Description: 蓝图文件
'''
from pathlib import Path
import os,sys
sys.path.append(Path(os.path.dirname(__file__)).resolve().parent)
from . import admin
from flask import *
from flask import request, current_app, session, render_template, make_response, Response, abort
from utils.write_log import Sql_log
from typing import Any
from pydantic import BaseModel
from utils.func import *


@admin.route('/admin/', methods=['GET', 'POST'])
def admin_index():
    return render_template('admin_login.html')


@admin.route('/admin/log/', methods=['GET'])
def admin_log():
    return render_template('admin_log.html')


@admin.route('/admin/log/pageLoadJson/', methods=['GET', 'POST'])
@error_return_501
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


@admin.route('/admin/log/rm_all_log/', methods=['GET', 'POST'])
@dontreturn
def rm_all_log():
    '''删除所有日志数据的接口,需要提供key'''
    req = request_parse(request)
    log = Sql_log()
    key = req.get('key')
    if key == 'lovehyy':
        log.rm_all_log()
        return resp_parse(BaseResp(code=200,msg='已删除整个日志数据库'))
    return resp_parse(BaseResp(code=502,msg='删除失败Key错误'))

