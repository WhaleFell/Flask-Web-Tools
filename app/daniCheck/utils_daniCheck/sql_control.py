# !/usr/bin/python python3
# coding=utf-8
'''
Author: whalefall
Date: 2021-08-19 18:46:02
LastEditTime: 2021-08-25 12:49:02
Description: 数据库操作
'''
from pathlib import Path
import os
import sqlite3
from pydantic import BaseModel
from typing import Optional, Union


class Info(BaseModel):
    student_sfz: Optional[str]
    student_name: Optional[str]
    student_pyname: Optional[str]
    student_where: Optional[str]
    student_born: Optional[str]
    student_class: Union[int, str] = None
    student_photo: Union[str, None] = None
    parent_name: Optional[str]
    parent_tel: Union[int, str] = None


# 项目的绝对目录
PROJECT_PATH = Path(os.path.abspath(os.path.dirname(__file__))).parent


class Sql(object):
    '''操作大沥高中数据库的类'''

    def __init__(self) -> None:
        db_path = Path().joinpath(PROJECT_PATH, 'db', 'data.db')
        print(db_path)
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.curson = self.conn.cursor()
        self.start()

    def start(self):
        '''初始化数据库'''
        sql = '''
CREATE TABLE IF NOT EXISTS info (
    student_sfz TEXT PRIMARY KEY NOT NULL,
    student_name TEXT NOT NULL,
    student_py TEXT NULL,
    student_where TEXT NULL,
    student_born TEXT NULL,
    student_class INT NULL,
    student_photo TEXT NOT NULL,
    parent_name TEXT NULL,
    parent_tel INT NULL
    );
'''
        self.curson.execute(sql)
        self.conn.commit()

    def insert(self, info: Info):
        '''传入一个数据集对象,写入数据库'''
        sql = f'''
        INSERT INTO info (student_sfz,student_name,student_class,student_photo,parent_name,parent_tel)
        VALUES ('{info.student_sfz}', '{info.student_name}', '{info.student_class}',
                '{info.student_photo}','{info.parent_name}','{info.parent_tel}');
        '''

        try:
            self.curson.execute(sql)
            self.conn.commit()
            print(f"写入成功{info}")
        except Exception as e:
            print(f"{info}写入数据库时出错:{e}")

    def update(self, info: Info):
        '''根据身份证,更新信息,传入info数据集'''
        sql = f'''
        UPDATE info
        SET parent_name = '{info.parent_name}',parent_tel = '{info.parent_tel}'
        WHERE student_sfz = '{info.student_sfz}' AND parent_name = 'None';
        '''
        try:
            self.curson.execute(sql)
            self.conn.commit()
            print(f"更新成功{info}")
        except Exception as e:
            print(f"更新数据库时出错:{e}")

    def search(self, info: Info, type="name"):
        '''查询语句,支持类型查询,默认名字'''
        switch = {
            "name": f"SELECT * FROM info WHERE student_name LIKE '%{info.student_name}%';",
            "born": f"SELECT * FROM info WHERE student_born='{info.student_born}';",
            "pyname": f"SELECT * FROM info WHERE student_pyname='{info.student_pyname}';",
            "sfz": f"SELECT * FROM info WHERE student_sfz='{info.student_sfz}';",
        }
        sql = switch.get(type)
        if not sql:
            sql = switch['name']

        try:
            self.curson.execute(sql)
            # self.curson.fetchall()
            # return [data for data in self.curson.fetchall()]
            l = []
            for data in self.curson.fetchall():
                # print(data)
                d = Info(
                    student_sfz=data[0],
                    student_name=data[1],
                    student_pyname=data[2],
                    student_where=data[3],
                    student_born=data[4],
                    student_class=data[5],  # 可选参数,不传入时默认none
                    student_photo=data[6],
                    parent_name=data[7],
                    parent_tel=data[8]
                )
                l.append(d)
            # print(l)
            return l

        except Exception as e:
            print(f"查询数据库时出错:{e}")

    def addWhere(self, info: Info):
        '''根据身份证写入身份证地址和生日'''
        sql = f'''
    UPDATE info
SET student_where = '{info.student_where}',
student_born = '{info.student_born}'
WHERE
	student_sfz = '{info.student_sfz}';
    '''
        try:
            self.curson.execute(sql)
            self.conn.commit()
            print(f"更新成功{info}")
        except Exception as e:
            print(f"{info}更新数据库时出错:{e}")

    def addPyname(self, info: Info):
        '''增加拼音'''
        sql = f'''
    UPDATE info
SET student_pyname = '{info.student_pyname}'
WHERE
	student_sfz = '{info.student_sfz}';
    '''
        try:
            self.curson.execute(sql)
            self.conn.commit()
            print(f"更新成功{info}")
        except Exception as e:
            print(f"{info}更新数据库时出错:{e}")

    def __del__(self) -> None:
        print(f"数据库操作:{self.conn.total_changes}行,正在关闭ing")
        self.conn.close()


if __name__ == '__main__':
    # print(PROJECT_PATH)
    sqlbot = Sql()
    # print(Path.cwd())
    i = Info(student_sfz=441224200512252924,
             student_where="11", student_born="111")
    print(sqlbot.search(Info(student_name="黄")))
