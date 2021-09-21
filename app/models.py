#!/usr/bin/python python3
# coding=utf-8
"""
Author: whalefall
Date: 2021-09-20 12:01:45
LastEditTime: 2021-09-20 12:14:33
Description: 数据库模型,及返回api的basemodels模型
"""
from . import db
from . import login_manager
from flask_login import UserMixin
from pydantic import BaseModel
from typing import Optional, Union, List
from datetime import datetime
import pytz


def getCNtimestamp() -> int:
    """获取中国的时间戳"""
    tz = pytz.timezone('Asia/Shanghai')
    return int(datetime.now(tz).timestamp())


def timestamp2time(epoch: int) -> str:
    """将时间戳转为中国人类可读时间"""
    epoch = int(epoch)
    tz = pytz.timezone('Asia/Shanghai')
    dt = pytz.datetime.datetime.fromtimestamp(epoch, tz)
    return dt.strftime('%Y-%m-%d %H:%M:%S')


@login_manager.user_loader
def load_user(user_id):
    """用户加载,获取已登录用户的信息使用,传入用户识别符"""
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    """用户储存模型"""
    __tablename__ = 'users'
    id = db.Column(db.INTEGER, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(64))


class Log(db.Model):
    """日志储存模型"""
    __tablename__ = 'logs'
    __table_args__ = {'extend_existing': True}  # 防止冲突
    timestamp = db.Column(db.INT, primary_key=True, nullable=False, default=lambda: getCNtimestamp())
    ip = db.Column(db.String(64), nullable=True)
    ip_addr = db.Column(db.String(64), nullable=True)
    gps_addr = db.Column(db.String(64), nullable=True)
    base64_pic = db.Column(db.TEXT, nullable=True)

    # 把SQLAlchemy查询对象(单个)转换成字典,并添加一个可读时间字段
    # 当多个查询对象以列表组合的话要先遍历再使用哦
    def to_dict(self):
        r_dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        r_dict['read_time'] = timestamp2time(r_dict['timestamp'])
        return r_dict


class StudentInfo(db.Model):
    """学生数据模型"""
    __tablename__ = 'info'
    __table_args__ = {'extend_existing': True}  # 防止冲突
    student_sfz = db.Column(db.TEXT, primary_key=True)
    student_name = db.Column(db.TEXT)
    student_pyname = db.Column(db.TEXT)
    student_where = db.Column(db.TEXT)
    student_born = db.Column(db.TEXT)
    student_class = db.Column(db.INT)
    student_photo = db.Column(db.TEXT)
    parent_name = db.Column(db.TEXT)
    parent_tel = db.Column(db.INT)

    # 把SQLAlchemy查询对象转换成字典
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class StudentInfoModel(BaseModel):
    """学生信息模型,供旧API使用"""
    student_sfz: Optional[str]
    student_name: Optional[str]
    student_pyname: Optional[str]
    student_where: Optional[str]
    student_born: Optional[str]
    student_class: Union[int, str] = None
    student_photo: Union[str, None] = None
    parent_name: Optional[str]
    parent_tel: Union[int, str] = None


class Repo(BaseModel):
    """API返回格式"""
    code: int = 200  # 状态码 200->成功
    msg: str  # 信息
    data: List = []
