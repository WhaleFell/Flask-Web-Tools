#!/usr/bin/python python3
# coding=utf-8
'''
Author: whalefall
Date: 2021-08-23 15:08:21
LastEditTime: 2021-08-26 17:49:12
Description: 中国居民身份证解析模块
'''

# from daniCheck.views import index
from pathlib import Path
import pandas
from pydantic import BaseModel
import datetime
from typing import Union


class ParseIdResult(BaseModel):
    '''解析返回的数据'''
    where: str = "地球"  # 身份证归属地
    born: str = None  # 出生日期格式 xxxx年xx月xx日
    age: Union[float, str] = None  # 当前年龄(保留两位小数,单位岁)
    sex: str = None
    starType: str = None  # 星座
    shuxian: str = None  # 属相




def dontreturn(func):
    '''防止函数错误的装饰器'''
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return None
    return inner


class GetInformation(object):
    '''处理身份证信息的类'''

    def __init__(self, id):
        self.id = id
        self.birth_year = self.id[6:10]
        self.birth_month = self.id[10:12]
        self.birth_day = self.id[12:14]

    @dontreturn
    def get_birthday(self):
        """通过身份证号获取出生日期"""
        birthday = "{0}-{1}-{2}".format(self.birth_year,
                                        self.birth_month, self.birth_day)
        dataclass = datetime.datetime.strptime(
            birthday, "%Y-%m-%d")
        return birthday

    @dontreturn
    def get_sex(self):
        """男生：1 女生：2"""
        num = int(self.id[16:17])
        if num % 2 == 0:
            return "女"
        else:
            return "男"

    @dontreturn
    def get_age(self) -> float:
        """通过身份证号获取年龄"""
        birthday = self.get_birthday()
        dataclass = datetime.datetime.strptime(
            birthday, "%Y-%m-%d")
        now = datetime.datetime.now()
        d = (now-dataclass).days
        age = round(float(d/365), 2)
        return age

    @dontreturn
    def get_star(self) -> str:
        '''获取星座'''
        month = int(self.birth_month)
        date = int(self.birth_day)
        dates = (21, 20, 21, 21, 22, 22, 23, 24, 24, 24, 23, 22)
        constellations = ("摩羯", "水瓶", "双鱼", "白羊", "金牛", "双子",
                          "巨蟹", "狮子", "处女", "天秤", "天蝎", "射手", "摩羯")
        if date < dates[month-1]:
            return constellations[month-1]
        else:
            return constellations[month]

    @dontreturn
    def zodiacYear(self):
        '''根据年份获取属相'''
        zodiacs = ['猴', '鸡', '狗', '猪', '鼠', '牛', '虎', '兔', '龙', '蛇', '马', '羊']
        year = self.birth_year
        n = int(year) % 12
        for i in range(12):
            if n == i:
                # print('你的属相是:' + zodiacs[i])
                return zodiacs[i]


# csv文件路径
CSV_PATH = Path(__file__).resolve().parent.parent.joinpath('db', 'ID.csv')

df = pandas.read_csv(CSV_PATH)


def parseID(idcard: str) -> ParseIdResult:
    '''传入居民身份证返回解析结果'''
    paresBot = GetInformation(idcard)
    try:
        whereID = int(idcard[0:6])  # 获取前6位
        # print(whereID)
        data = df.loc[df['id'] == whereID, ]
        where = data['province'].to_string(
            index=None)+data['city'].to_string(index=None)+data["county"].to_string(index=None)
    except Exception as e:
        where = "地球"
        print("获取归属地错误!", e)

    r = {
        "where": where,
        "born": paresBot.get_birthday(),
        "age": paresBot.get_age(),
        "sex": paresBot.get_sex(),
        "starType": paresBot.get_star(),
        "shuxian": paresBot.zodiacYear()
    }

    return ParseIdResult(**r)


if __name__ == "__main__":
    # parseID("440102200511135633")
    # print(GetInformation(id).zodiacYear())

    print(parseID(id).dict())
