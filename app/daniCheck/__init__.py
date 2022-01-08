#!/usr/bin/python python3
# coding=utf-8
"""
Author: whalefall
Date: 2021-08-20 03:08:15
LastEditTime: 2021-08-23 00:35:55
Description: 大沥查人蓝图
"""
from flask import Blueprint

dani = Blueprint('dani', __name__,template_folder='templates')

from . import views
