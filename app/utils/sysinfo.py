#!/usr/bin/python python3
# coding=utf-8
'''
Author: whalefall
Date: 2021-08-20 10:51:53
LastEditTime: 2021-08-20 12:23:51
Description: 获取系统信息
'''
import datetime
import time
import psutil
from pydantic import BaseModel


class SystemInfo(BaseModel):
    code: int = 200
    msg: str = "获取成功!"
    cpu_status: str = None
    percent_nc: int = None
    uptime: str = None


def get_memory_info():
    memory = psutil.virtual_memory()
    total_nc = round((float(memory.total) / 1024 / 1024 / 1024), 3)  # 总内存
    used_nc = round((float(memory.used) / 1024 / 1024 / 1024), 3)  # 已用内存
    percent_nc = memory.percent  # 内存使用率

    # return "%s/%s (%s%)" % (used_nc, total_nc, percent_nc)
    return f"{used_nc}GB/{total_nc}GB ({percent_nc}%)", percent_nc


def uptime():
    now = time.time()
    boot = psutil.boot_time()
    boottime = datetime.datetime.fromtimestamp(
        boot).strftime("%Y-%m-%d %H:%M:%S")
    nowtime = datetime.datetime.fromtimestamp(
        now).strftime("%Y-%m-%d %H:%M:%S")
    up_time = str(
        datetime.datetime.utcfromtimestamp(now).replace(microsecond=0)
        - datetime.datetime.utcfromtimestamp(boot).replace(microsecond=0)
    )
    alltime = (boottime, nowtime, up_time)
    return "已经运行了%s" % up_time


def sysinfo() -> SystemInfo:
    try:
        mem_info, percent_nc = get_memory_info()
        up_time = uptime()
        s = SystemInfo(cpu_status=mem_info, uptime=up_time,
                       percent_nc=percent_nc)
    except Exception as e:
        s = SystemInfo(code=501, msg="获取失败!%s" % e)
    finally:
        return s


if __name__ == '__main__':
    print(sysinfo())
