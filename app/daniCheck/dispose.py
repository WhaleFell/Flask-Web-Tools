#!/usr/bin/python python3
# coding=utf-8
'''
Author: whalefall
Date: 2021-08-24 12:56:11
LastEditTime: 2021-08-27 14:46:50
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
import asyncio
import aiofiles

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


async def download(url: str):
    '''异步下载图片并保存到文件夹下'''
    file_name = url.split('/')[-1]
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.9 Safari/537.36",
    }
    try:
        async with httpx.AsyncClient(headers=header) as c:
            resp = await c.get(url)
            # assert resp.status_code == 200
            async with aiofiles.open(f'E:/daniStudentPic/{file_name}', "wb") as f:
                await f.write(resp.read())
                print(f"{file_name}下载成功")
    except Exception as e:
        print(f'{url}下载错误！', e)


async def main(i):  # 封装多任务的入口函数
    # 用列表表达式创建任务
    tasks = [
        asyncio.ensure_future(download(url))
        for url in i
    ]
    await asyncio.gather(*tasks)


def download_pic():
    '''图片私有化,防止未来的某天地球爆炸了图片不见了或者改变了.'''
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.9 Safari/537.36",
    }
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    sql = '''
    SELECT student_photo FROM info;
    '''
    cursor.execute(sql)
    urlList = []
    # 弃用异步下载方式
    # for data in cursor.fetchall():
    #     url = data[0]
    #     if url != None:
    #         url_row = f"https://ares-k12.weds.com.cn/{url}"
    #         urlList.append(url_row)
    # print(f"一共有{len(urlList)}张图片")
    # # print(urlList)
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main(urlList))
    # E:/daniStudentPic/ 下载目录

    for data in cursor.fetchall():
        url = data[0]
        if url != "None":
            url_row = f"https://ares-k12.weds.com.cn/{url}"
            urlList.append(url_row)
    print(urlList)
    print(f"一共有{len(urlList)}张图片")

    # with httpx.Client(headers=header) as client:
    #     for url in urlList:
    #         try:
    #             resp = client.get(url)
    #             file_name = url.split('/')[-1]
    #             with open(f'E:/daniStudentPic/{file_name}', "wb") as p:
    #                 p.write(resp.read())
    #             print(f"{file_name}下载成功")
    #         except Exception as e:
    #             print(f"{url} 下载失败：{e}")


if __name__ == '__main__':
    # main()
    # print(get_pyname('黄颖怡'))
    # mianPyname()
    download_pic()
