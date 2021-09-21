#!/usr/bin/python python3
# coding=utf-8
"""
Author: whalefall
Date: 2021-09-21 11:57:50
LastEditTime: 2021-09-21 12:03:41
Description: 登录表单类
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField,ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo
from ..models import User
from flask import flash


class LoginForm(FlaskForm):
    """登录表单,账号不为空"""
    user = StringField('账号:', validators=[DataRequired()])
    password = PasswordField('密码:', validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('Submit')


class RegistrathionFrom(FlaskForm):
    """注册表单"""
    email = StringField("邮箱", validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('用户名', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('密码', validators=[DataRequired(), EqualTo('password2', message='两次输入的密码不一致!')])
    password2 = PasswordField('再次输入密码', validators=[DataRequired()])
    submit = SubmitField('注册')

    # 在表单类创建自定义的验证函数 validate_ 开头
    # ValidationError从wtforms导入，用来向用户显示错误信息
    def validate_email(self, field):
        """自定义表单类函数(自动验证),验证邮箱是否被注册,传入表单对象"""
        if User.query.filter_by(email=field.data).first():
            # raise ValidationError('该邮箱已被注册!')
            flash('该邮箱已被注册!')

    def validate_username(self, field):
        """自定义表单类函数,验证邮箱是否被注册,传入表单对象"""
        if User.query.filter_by(username=field.data).first():
            # raise ValidationError('该用户名已被注册!')
            flash('该用户名已被注册!')