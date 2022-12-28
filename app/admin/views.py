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
from flask import request, current_app, session, render_template, make_response, Response, abort, redirect, url_for
from ..utils.func import error_return_501, dontreturn, request_parse, resp_parse, BaseResp
from ..models import Log, db, User
from .forms import LoginForm, RegistrathionFrom
from flask_login import login_user, login_required


@admin.route('/admin/', methods=['GET', 'POST'])
def admin_index():
    form = LoginForm()
    if form.validate_on_submit():
        '''提交表单'''
        user = User.query.filter_by(username=form.user.data).first()
        if user is not None and user.password == form.password.data:
            """通过后登录用户"""
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('admin.admin_log'))

        flash("登录失败,请检查账号或密码")
        # 清空表单字段,防止再次渲染有数据
        form.user.data = ''
        form.password.data = ''
    return render_template('admin/admin_login.html', form=form)


@admin.route('/register/', methods=['GET', 'POST'])
def register():
    """注册新用户"""
    form = RegistrathionFrom()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        print(f"用户{form.username.data}注册")
        flash("注册成功,你可以登录了!")
        return redirect(url_for('admin.admin_index'))
    return render_template('admin/register.html', form=form)


@admin.route('/admin/log/', methods=['GET'])
@login_required
def admin_log():
    """日志查看路由,登录保护"""
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
@login_required
@dontreturn
def rm_all_log():
    """删除所有日志数据的接口,需要提供key"""
    req = request_parse(request)
    key = req.get('key')
    if key == 'cyxdsb':
        db.session.execute('delete from logs;')
        db.session.commit()
        return resp_parse(BaseResp(code=200, msg='已删除整个日志数据库'))
    return resp_parse(BaseResp(code=502, msg='删除失败Key错误'))
