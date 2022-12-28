#!/usr/bin/python python3
# coding=utf-8
"""
Author: WhaleFall
Date: 2021-08-20 03:12:38
LastEditTime: 2021-08-29 11:03:56
Description: 大沥查人视图函数
"""
from flask import request, abort, make_response, render_template
from ..utils.func import resp_parse, request_parse
from ..utils.parse_idcard import parseID
from ..models import StudentInfo, Repo
from . import dani


# 大沥查人首页

def login(func):
    """验证session装饰器"""

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
    resp = make_response(render_template('daniCheck/check.html'))
    resp.set_cookie("from", "index")

    return resp


# 大沥查人api接口
switch = {
    "name": lambda value: StudentInfo.query.filter(StudentInfo.student_name.like('%' + value + '%')).all(),
    "born": lambda value: StudentInfo.query.filter_by(student_born=value).all(),
    "pyname": lambda value: StudentInfo.query.filter_by(student_pyname=value).all(),
    "sfz": lambda value: StudentInfo.query.filter_by(student_sfz=value).first_or_404().to_dict(),
}


@dani.route('/dani/api/', methods=['GET', 'POST'])
@login
def api():
    req_data = request_parse(request)
    value = req_data.get('value')
    search_type = req_data.get('type', 'name')

    if value:
        i = switch.get(search_type)(value)  # 数据库查询返回的是一个查询对象列表
        result = []
        for r in i:
            result.append(r.to_dict())

        if not result:
            r = Repo(code=202, msg=f"按{search_type}查{value}结果为空!")
        else:
            r = Repo(
                msg=f"按{search_type}查{value}共有{len(result)}条结果", data=result)

        return resp_parse(r)

    return resp_parse(Repo(code=201, msg="请传入value参数"))


@dani.route('/dani/<idcard>/', methods=['GET'])
def more(idcard):
    """学生详细页视图,调用身份证查询"""
    r = switch.get('sfz')(idcard)
    if not r:
        abort(404)
    r_p = parseID(idcard)
    kw = {
        "info": r,
        "info2": r_p.dict()
    }
    return render_template('daniCheck/more.html', **kw)
