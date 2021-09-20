#!/usr/bin/python python3
# coding=utf-8
'''
Author: whalefall
Date: 2021-08-29 11:00:52
LastEditTime: 2021-08-29 11:03:03
Description: flask常用的方法
'''
from pydantic import BaseModel
from typing import Any
from functools import wraps
import json
from flask import Response, request, abort


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


class RespUpload(BaseModel):
    '''上传base64图片的响应信息'''
    code: int = 200
    msg: str


class BaseResp(BaseModel):
    '''响应的主要格式'''
    code: int = 200  # 响应代码
    msg: str = None  # 响应信息
    data: Any = None  # 响应信息


def error_return_501(func):
    '''函数如果错误就返回501'''

    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            abort(501)

    return inner


def dontreturn(func):
    """函数如果错误就返回原因与请求的装饰器,修复装饰器视图函数名重复的bug"""

    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return resp_parse(BaseResp(code=201, msg=f'通用接口错误,{e}'))

    return inner
