#!/usr/bin/python python3
# coding=utf-8
'''
Author: whalefall
Date: 2021-09-04 01:50:08
LastEditTime: 2021-09-04 02:35:00
Description: 数据库模型类
'''
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import os,sys
from pathlib import Path
sys.path.append(Path(os.path.dirname(__file__)).resolve().parent)
from app import *

db = SQLAlchemy(app)

class User(db.Model, UserMixin):  # 表名将会是 user
    name = db.Column(db.String(20), primary_key=True)  # 用户名
    pwd = db.Column(db.String(20))  # 密码

db.init_app(app)

# db.create_all()
# a1 = User(name='admin1', pwd='admin')
# db.session.add(a1)
# db.session.commit()
