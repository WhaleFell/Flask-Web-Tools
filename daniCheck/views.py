#!/usr/bin/python python3
# coding=utf-8
'''
Author: whalefall
Date: 2021-08-20 03:12:38
LastEditTime: 2021-08-25 13:35:20
Description: 大沥查人视图函数
'''
import os
import sys
sys.path.append(os.getcwd())
import json
from typing import List, Dict
from pydantic import BaseModel
from .utils_daniCheck.sql_control import Sql, Info
from flask import jsonify, request, current_app, session, render_template, make_response, Response, abort
from flask import *
from . import dani
from utils.parse_idcard import parseID


sql = Sql()


class Repo(BaseModel):
    code: int = 200  # 状态码 200->成功
    msg: str  # 信息
    data: List[
        Info
    ] = []


def resp_parse(resp):
    '''BaseModel类型返回json'''
    return Response(json.dumps(resp.dict(), ensure_ascii=False, sort_keys=False), mimetype='application/json')


def request_parse(req_data):
    '''解析请求数据并以json形式返回'''
    if req_data.method == 'POST':
        data = req_data.json
    elif req_data.method == 'GET':
        data = req_data.args

    return data

# 大沥查人首页


def login(func):
    '''验证session装饰器'''
    def auth(*args, **kwargs):
        # if session.get('from') == 'index':
        #     # Flask 要返回原函数以便路由再修饰
        #     return func(*args, **kwargs)
        # else:
        #     abort(401)
        if request.cookies.get('from') == 'index':
            # Flask 要返回原函数以便路由再修饰
            return func(*args, **kwargs)
        else:
            abort(401)

    return auth


@dani.route('/dani/', methods=['GET'])
def index():
    # 设置session
    # session['from'] = 'index'
    resp = make_response(render_template('check.html'))
    resp.set_cookie("from", "index")

    return resp

# 大沥查人api接口


@dani.route('/dani/api/', methods=['GET', 'POST'])
@login
def api():
    req_data = request_parse(request)
    value = req_data.get('value')
    search_type = req_data.get('type')
    switch = {
        "name": Info(student_name=value),
        "born": Info(student_born=value),
        "pyname": Info(student_pyname=value),
        "sfz": Info(student_sfz=value),
    }

    if value:
        i = switch.get(search_type)
        if not i:
            search_type = "name"
            i = switch.get('name')

        result = sql.search(i, type=search_type)
        if result == []:
            r = Repo(code=202, msg=f"按{search_type}查{value}结果为空!")
        else:
            r = Repo(
                msg=f"按{search_type}查{value}共有{len(result)}条结果", data=result)
        # return jsonify(r.dict())
        return resp_parse(r)

    return resp_parse(Repo(code=201, msg="请传入value参数"))


@dani.route('/dani/<idcard>/', methods=['GET'])
def more(idcard):
    '''学生详细页视图,调用身份证查询'''
    i = Info(student_sfz=idcard)
    r = sql.search(i,type="sfz")
    if r == []:
        abort(404)
    r_p = parseID(idcard)
    kw = {
        "info": r[0].dict(),
        "info2":r_p.dict()
    }
    print(kw)
    return render_template('more.html', **kw)
