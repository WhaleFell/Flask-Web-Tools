#!/usr/bin/python python3
# coding=utf-8
"""
Author: whalefall
Date: 2021-09-20 11:08:25
LastEditTime: 2021-09-20 13:47:21
Description: Flask应用配置文件
"""
import os
import platform

basedir = os.path.abspath(os.path.dirname(__file__))  # 项目绝对路径


class Config(object):
    '''基类Config,每个子类可以分别定义配置'''
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'lovehyypzezxiqiao1111'  # 密钥
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 数据库
    FLASK_DEBUG = True
    SESSION_TYPE = 'filesystem'  # session 模式
    JSON_AS_ASCII = False  # 禁止json中文自动转码
    PERMANENT_SESSION_LIFETIME = 10  # session超时时间

    # 下面是 GitHub 配置
    UPLOAD_PIC = True  # 是否开启图片上传GitHub
    GITHUB_TOKEN = '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'  # GitHub令牌(示例,已取消)
    USERNAME = 'AdminWhaleFall'
    REPO = 'pic'  # 储存仓库名
    REPO_PATH = 'catch_pic'  # 储存仓库路径

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    """开发配置"""
    FLASK_DEBUG = True
    HOST = "0.0.0.0"
    # 判断操作系统拼接数据库地址
    if platform.system().lower() == 'windows':
        SQLALCHEMY_DATABASE_URI = os.environ.get(
            'DEV_DATABASE_URL') or 'sqlite:///'+os.path.join(basedir, 'db/dev_data.db')

    elif platform.system().lower() == 'linux':
        SQLALCHEMY_DATABASE_URI = os.environ.get(
            'DEV_DATABASE_URL') or 'sqlite:///'+os.path.join(basedir, 'db/dev_data.db')


config = {
    'default': DevelopmentConfig
}
