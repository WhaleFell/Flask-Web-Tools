#!/usr/bin/python python3
# coding=utf-8
'''
Author: whalefall
Date: 2021-08-26 16:12:04
LastEditTime: 2021-08-27 17:37:38
Description: 利用sqlite写入日志文件.
'''
from pathlib import Path
import os
import sqlite3
from pydantic import BaseModel
from typing import Any, List, Optional, Union
import time
import pytz
from datetime import datetime


class SeeInfo(BaseModel):
    timestamp: int
    read_time: Optional[str]
    ip: str
    ip_addr: Optional[str]
    gps_addr: Optional[str]
    base64_pic: Optional[str]


# 项目的绝对目录
PROJECT_PATH = Path(os.path.abspath(os.path.dirname(__file__))).parent


class Sql_log(object):
    '''操作日志数据库的类'''

    def __init__(self) -> None:
        self.db_path = Path().joinpath(PROJECT_PATH, 'db', 'log.db')
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.curson = self.conn.cursor()
        self.start()

    def start(self):
        '''初始化数据库'''
        sql = '''
CREATE TABLE IF NOT EXISTS log (
    timestamp INT PRIMARY KEY NOT NULL,
    ip TEXT NULL,
    ip_addr TEXT NULL,
    gps_addr TEXT NULL,
    base64_pic BLOB NULL
    );
'''
        self.curson.execute(sql)
        self.conn.commit()

    def insert(self, info: SeeInfo):
        '''传入一个数据集对象,写入数据库'''
        sql = f'''
        INSERT INTO log (timestamp, ip, ip_addr, gps_addr, base64_pic)
        VALUES ({info.timestamp}, '{info.ip}', '{info.ip_addr}', '{info.gps_addr}',
                '{info.base64_pic}');
        '''

        try:
            self.curson.execute(sql)
            self.conn.commit()
            # print(f"写入成功{info}")
        except Exception as e:
            print(f"{info}写入日志数据库时出错:{e}")

    def count(self) -> int:
        '''查询数据库总条数'''
        sql = '''
        select count(*) from log;
        '''
        try:
            self.curson.execute(sql)
            r = self.curson.fetchall()[0][0]
            print(f"日志数据库条数{r}")
            return r

        except Exception as e:
            print(f"查询日志数据库个数时出错:{e}")

    def search(self, start: int, count: int) -> List[SeeInfo]:
        """sqlite3 分页查询
        select * from log order by timestamp limit 10 offset 0;
        offset代表从第几条记录“之后“开始查询，limit表明查询多少条结果 DESC降序排列;
        查询时间时自动把时间戳转为人类可读时间.
        """
        sql = f'''
        select * from log order by timestamp DESC limit {count} offset {start};  
        '''
        try:
            self.curson.execute(sql)
            r = self.curson.fetchall()
            # print(r)
            datas = []
            for data in r:
                d = {
                    "timestamp": data[0],
                    "read_time": timestamp2time(data[0]),
                    "ip": data[1],
                    "ip_addr": data[2],
                    "gps_addr": data[3],
                    "base64_pic": data[4],
                }
                s = SeeInfo(**d)
                datas.append(s)
            # print(datas)
            return datas

        except Exception as e:
            print(f"查询日志数据库时出错:{e}")

    def rm_all_log(self):
        '''！删除整个数据表！危险操作！'''
        sql = '''
        delete from log;
        '''
        self.curson.execute(sql)
        self.conn.commit()
        print(f"清空数据表成功！")

    def __del__(self) -> None:
        print(f"日志数据库操作:{self.conn.total_changes}行,正在关闭ing")
        self.conn.close()


def timestamp2time(epoch: int) -> str:
    '''将时间戳转为中国人类可读时间'''
    tz = pytz.timezone('Asia/Shanghai')
    dt = pytz.datetime.datetime.fromtimestamp(epoch, tz)
    return dt.strftime('%Y-%m-%d %H:%M:%S')


def getCNtimestamp() -> int:
    '''获取中国的时间戳'''
    tz = pytz.timezone('Asia/Shanghai')
    return int(datetime.now(tz).timestamp())


if __name__ == '__main__':
    r = getCNtimestamp()
    print(r)
    print(timestamp2time(r))
    pass
