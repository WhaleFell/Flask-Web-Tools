#!/usr/bin/python python3
# coding=utf-8
"""
Author: whalefall
Date: 2021-08-26 17:16:44
LastEditTime: 2021-08-26 17:18:45
Description: 蓝图包初始化
"""
from flask import *
from flask import Blueprint

admin = Blueprint('admin', __name__, template_folder='templates')

from . import views
