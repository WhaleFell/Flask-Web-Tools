#!/usr/bin/python python3
# coding=utf-8
'''
Author: whalefall
Date: 2021-08-26 17:16:53
LastEditTime: 2021-08-27 17:34:26
Description: 蓝图文件
'''
from . import admin
from flask import *
from flask import request, current_app, session, render_template, make_response, Response, abort
from utils.write_log import Sql_log
from typing import Any
from pydantic import BaseModel


def return_501(func):
    '''函数如果错误就返回501'''
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            abort(501)
    return inner

def dontreturn(func):
    '''函数如果错误就返回原因与请求的装饰器'''
    def inner1(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return resp_parse(BaseResp(code=201, msg=f'通用接口错误,{e}'))
    return inner1

def resp_parse(resp):
    '''BaseModel类型返回json'''
    return Response(json.dumps(resp.dict(), ensure_ascii=False, sort_keys=False), mimetype='application/json')


def request_parse(req_data) -> dict:
    '''解析请求数据并以字典的形式返回'''
    if req_data.method == 'POST':
        data = req_data.form

    elif req_data.method == 'GET':
        data = req_data.args

    return dict(data)

class BaseResp(BaseModel):
    '''响应的主要格式'''
    code: int = 200  # 响应代码
    msg: str = None  # 响应信息
    data: Any = None  # 响应信息

@admin.route('/admin/', methods=['GET', 'POST'])
def admin_index():
    return render_template('admin_login.html')


@admin.route('/admin/log/', methods=['GET'])
def admin_log():
    return render_template('admin_log.html')


@admin.route('/admin/log/pageLoadJson/', methods=['GET', 'POST'])
@return_501
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

