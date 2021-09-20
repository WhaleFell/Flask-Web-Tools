#!/usr/bin/python python3
# coding=utf-8
'''
Author: whalefall
Date: 2021-09-20 13:03:27
LastEditTime: 2021-09-20 13:27:03
Description: 测试单元
'''
import unittest

from flask import current_app

from app import create_app,db

class basicsTestCase(unittest.TestCase):
    '''测试实例'''

    def setUp(self) -> None:
        '''尝试创建一个测试环境'''
        # 用开发配置创建应用,激活上下文,确保在测试中使用 `current_app`
        self.app = create_app('default')
        self.app_context=self.app.app_context()
        # 上下文被推送后,就可以在该线程使用全局上下文变量,pop弹出后就不能使用
        self.app_context.push()
        # 创建数据库
        db.create_all()

    def tearDown(self) -> None:
        '''测试完成后删除数据库和弹出应用上下文'''
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_app_exists(self):
        self.assertFalse(create_app is None)
    
    def test_app_is_testing(self):
        pass

        

