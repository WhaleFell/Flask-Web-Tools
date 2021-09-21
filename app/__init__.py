#!/usr/bin/python python3
# coding=utf-8
"""
Author: whalefall
Date: 2021-08-23 15:25:37
LastEditTime: 2021-09-20 13:45:12
Description: APP包工厂函数
"""
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config

# 实例化数据库全局对象
db = SQLAlchemy()
# 实例化登录对象
login_manager = LoginManager()
login_manager.login_view = 'admin.admin_index'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)  # 配置类中的初始化

    db.init_app(app)
    login_manager.init_app(app)

    # 注册蓝本
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .daniCheck import dani
    app.register_blueprint(dani)

    from .admin import admin
    app.register_blueprint(admin)

    return app
