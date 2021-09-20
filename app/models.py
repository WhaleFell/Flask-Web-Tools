#!/usr/bin/python python3
# coding=utf-8
'''
Author: whalefall
Date: 2021-09-20 12:01:45
LastEditTime: 2021-09-20 12:14:33
Description: 数据库模型,及返回api的basemodels模型
'''
from . import db


class Log(db.Model):
    '''日志储存模型'''
    __tablename__ = 'logs'
    timestamp = db.Column(db.DateTime, nullable=False)
    ip = db.Column(db.String(64), nullable=True)
    ip_addr = db.Column(db.String(64), nullable=True)
    gps_addr = db.Column(db.String(64), nullable=True)
    base64_pic = db.Column(db.LargeBinary, nullable=True)
