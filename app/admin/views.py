#!/usr/bin/python python3
# coding=utf-8
"""
Author: whalefall
Date: 2021-08-26 17:16:53
LastEditTime: 2021-08-29 11:04:13
Description: 蓝图文件
"""
from . import admin
from flask import *
from flask import request, current_app, session, render_template, make_response, Response, abort
from ..utils.func import error_return_501, dontreturn, request_parse, resp_parse, BaseResp
from ..models import Log, db


@admin.route('/admin/', methods=['GET', 'POST'])
def admin_index():
    return render_template('admin/admin_login.html')


@admin.route('/admin/log/', methods=['GET'])
def admin_log():
    return render_template('admin/admin_log.html')


@admin.route('/admin/log/pageLoadJson/', methods=['GET', 'POST'])
@dontreturn
def pageLoad():
    """提供数据查询分页支持
    前端将传入:  {'pageNumber': '1'当前页码, 'pageSize': '20'每页数量}
    """
    req = request_parse(request)
    pageSize = int(req['pageSize'])
    pageNumber = int(req['pageNumber'])
    count = Log.query.count()
    # (pageNumber - 1) * pageSize:从第几条记录“之后“开始查询
    # pageSize:返回多少结果
    r = Log.query.offset((pageNumber - 1) * pageSize).limit(pageSize)
    pagedata = {
        "pageSize": pageSize,
        "pageNumber": pageNumber,
        "totalRow": count,
        "totalPage": int(count / pageSize),
        "list": [
            res.to_dict()
            for res in r
        ],
    }
    return jsonify(pagedata)


@admin.route('/admin/log/rm_all_log/', methods=['GET', 'POST'])
@dontreturn
def rm_all_log():
    """删除所有日志数据的接口,需要提供key"""
    req = request_parse(request)
    key = req.get('key')
    if key == 'lovehyy':
        db.session.execute('delete from logs;')
        db.session.commit()
        return resp_parse(BaseResp(code=200, msg='已删除整个日志数据库'))
    return resp_parse(BaseResp(code=502, msg='删除失败Key错误'))
