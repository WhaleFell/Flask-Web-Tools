#!/usr/bin/python python3
# coding=utf-8
'''
Author: whalefall
Date: 2021-08-24 12:56:11
LastEditTime: 2021-08-25 11:36:04
Description: 数据库整理程序.
'''
import os
import sys
sys.path.append(os.getcwd())
import sqlite3
from retrying import retry
from typing import Union
import re
from pathlib import Path
import httpx
from utils.parse_idcard import parseID
from utils_daniCheck.sql_control import Sql, Info
from pypinyin import pinyin

# 数据库绝对路径
DB_PATH = Path(os.path.dirname(__file__)).joinpath('db/data.db')
print(DB_PATH)


@retry(stop_max_attempt_number=3)
def get_where(cardid: Union[str, int]) -> str:
    '''传入cardid以获取身份证归属地 爬虫:http://idcard.ttcha.net/'''
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.9 Safari/537.36",
        "Host": "idcard.ttcha.net",
        "Referer": "http://idcard.ttcha.net/",
    }
    with httpx.Client(headers=header) as r:
        resp = r.get('http://idcard.ttcha.net/')
        # 解析首页获取 token
        # var sign = '7317ec15d2b6496fd7c95a2b56f917406330d1b7b1016383b42ee1f7dee3b042'; # token的位置
        pat_token = re.compile(r"var sign = '(.*?)';")
        token = pat_token.findall(resp.text)
        assert token != [], "获取Token错误"
        # 拼接接口地址
        api = f'http://idcard.ttcha.net/index.php?m=index&action=getidcard&idcard={str(cardid)}&sign={token[0]}'
        api_result = r.get(url=api)
        assert api_result, f"api返回错误获取到的Token为:{token}"

    where = api_result.json().get('address')
    assert where, f"获取地点错误,{api_result.text}"
    return where


def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    sql = '''
    SELECT student_sfz FROM info;
    '''
    cursor.execute(sql)
    sqlbot = Sql()
    for data in cursor.fetchall():
        sfz = data[0]
        try:
            where = get_where(sfz)
        except Exception as e:
            where = None
            print(f"{sfz}处理失败:{e}")

        local_parse = parseID(sfz).dict()
        born = local_parse.get('born')
        i = Info(student_sfz=sfz, student_where=where, student_born=born)
        sqlbot.addWhere(i)


def get_pyname(name):
    '''传入名字获取名字拼音缩写'''
    import pypinyin
    result = pypinyin.pinyin(name, style=pypinyin.NORMAL)
    return ''.join([i[0][0] for i in result])


def mianPyname():
    '''增加拼音名字'''
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    sql = '''
    SELECT student_sfz,student_name FROM info;
    '''
    cursor.execute(sql)
    sqlbot = Sql()
    for data in cursor.fetchall():
        sfz = data[0]
        name = data[1]

        try:
            pyname = get_pyname(name)
        except Exception as e:
            pyname = None
            print(f"{sfz}处理失败:{e}")

        i = Info(student_sfz=sfz, student_pyname=pyname)
        sqlbot.addPyname(i)


if __name__ == '__main__':
    # main()
    # print(get_pyname('黄颖怡'))
    mianPyname()
