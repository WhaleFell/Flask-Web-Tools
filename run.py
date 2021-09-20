#!/usr/bin/python python3
# coding=utf-8
'''
Author: whalefall
Date: 2021-09-20 11:08:42
LastEditTime: 2021-09-20 14:01:20
Description: 顶级目录Flask应用运行文件
'''
import os
from app import create_app,db

app = create_app('default')

# 添加自定义命令,被装饰的函数名就是命令名
@app.cli.command
def test():
    '''运行测试'''
    import unittest
    tests = unittest.TestLoader().discover('tests') # 从文件夹加载测试
    # verbosity参数可以控制执行结果的输出，0 是简单报告、1 是一般报告、2 是详细报告。
    unittest.TextTestRunner(verbosity=2).run(tests) # 运行测试

if __name__ == '__main__':
    app.run()

