#!/usr/bin/python python3
# coding=utf-8
'''
Author: whalefall
Date: 2021-08-20 03:02:54
LastEditTime: 2021-08-23 01:55:19
Description: Flask主文件
'''
from flask import *
from daniCheck import dani
from flask import redirect, url_for, request, Response, render_template
from pathlib import Path
import base64
from pydantic import BaseModel
import time
from utils.sysinfo import sysinfo
from utils.uploadGithub import upload_catch_pic
import threading


class RespUpload(BaseModel):
    '''上传base64图片的响应信息'''
    code: int = 200
    msg: str


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config.from_pyfile('setting.py')

# 注册大沥查人蓝图
app.register_blueprint(dani)


def resp_parse(resp):
    '''BaseModel类型返回json'''
    return Response(json.dumps(resp.dict(), ensure_ascii=False), mimetype='application/json')


def request_parse(req_data) -> dict:
    '''解析请求数据并以json形式返回'''
    if req_data.method == 'POST':
        data = req_data.form

    elif req_data.method == 'GET':
        data = req_data.args

    return dict(data)


@app.errorhandler(401)
def authfail(e):
    return redirect('/static/401.jpg')


@app.route('/upload_base64pic', methods=["POST", "GET"])
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


@app.route('/sysinfo', methods=["GET"])
def _():
    return resp_parse(sysinfo())


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=9000)
