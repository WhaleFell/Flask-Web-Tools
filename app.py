#!/usr/bin/python python3
# coding=utf-8
'''
Author: whalefall
Date: 2021-08-20 03:02:54
LastEditTime: 2021-08-23 18:40:28
Description: Flask主文件
'''
from typing import Any, Union
from flask import *
from daniCheck import dani
from flask import redirect, url_for, request, Response, render_template
from pathlib import Path
import base64
from pydantic import BaseModel
import time
from utils.sysinfo import sysinfo
from utils.uploadGithub import upload_catch_pic
from utils.parse_idcard import parseID, ParseIdResult
import threading


class RespUpload(BaseModel):
    '''上传base64图片的响应信息'''
    code: int = 200
    msg: str


class BaseResp(BaseModel):
    '''响应的主要格式'''
    code: int = 200  # 响应代码
    msg: str = None  # 响应信息
    data: Any = None  # 响应信息


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config.from_pyfile('setting.py')

# 注册大沥查人蓝图
app.register_blueprint(dani)


def resp_parse(resp):
    '''BaseModel类型返回json'''
    return Response(json.dumps(resp.dict(), ensure_ascii=False, sort_keys=False), mimetype='application/json')


def request_parse(req_data) -> dict:
    '''解析请求数据并以字典的形式返回'''
    if req_data.method == 'POST':
        data = req_data.form

    elif req_data.method == 'GET':
        data = req_data.args

    return dict(data)


@app.errorhandler(401)
def authfail(e):
    return redirect('/static/401.jpg')


@app.route('/upload_base64pic/', methods=["POST", "GET"])
def upload():
    '''上传base64图片并保存到静态文件夹'''
    req_data = request_parse(request)
    base64_pic = req_data.get('base64')
    if base64_pic:
        try:
            pic_path = Path(app.config['PROJECT_PATH'], "static",
                            "catch")
            pic_path.mkdir(exist_ok=True)
            file_name = int(time.time())
            pic_path = pic_path.joinpath('%s.jpg' % (file_name))
            with open(pic_path, "wb") as p:
                p.write(base64.b64decode(base64_pic))
            r = RespUpload(code=200, msg="up suc!")
        except Exception as e:
            r = RespUpload(code=501, msg=f"Up error {e}")
        else:
            # 无异常的时候新建线程上传图片
            t = threading.Thread(target=upload_catch_pic,
                                 args=(pic_path, file_name,))
            t.start()
            print("上传线程已建立")
        finally:
            return resp_parse(r)

    return resp_parse(RespUpload(code=502, msg="无内容?"))


@app.route('/sysinfo/', methods=["GET"])
def _():
    '''获取系统信息返回'''
    return resp_parse(sysinfo())


@app.route('/', methods=['GET'])
def index():
    '''首页'''
    return render_template('index.html')

@app.route('/sfz/',methods=['GET'])
def _sfz():
    return render_template('sfz.html')


@app.route('/sfz/api/', methods=['GET', 'POST'])
def parse_id_card():
    '''解析身份证'''
    req = request_parse(request)
    idcard = req.get('idcard')
    if not idcard:
        return resp_parse(BaseResp(code=501, msg="请传入请求参数idcard"))
    try:
        r = parseID(idcard)
    except Exception as e:
        return resp_parse(BaseResp(code=501, msg=f"解析身份证[{idcard}]出现问题{e},请检查身份证格式!"))
    else:
        return resp_parse(BaseResp(code=200, msg=f"身份证[{idcard}]解析成功!", data=r.dict()))


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=9000)
