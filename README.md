# 查询系统部署

## 通过 Gunicorn 运行
```shell
gunicorn run:app -c gunicorn.conf.py
```

## 通过 Docker 镜像部署
```shell
# 构建镜像,-t 指定上下文目录,-f 指定 Dockerfile 文件
docker build -t danistd:laster .
# 进入 shell 检查镜像路径(可选)
docker run -ti --rm <DOCKER_IMAGE> sh

# 从阿里云镜像服务 pull images
docker pull registry.cn-guangzhou.aliyuncs.com/danistd/danistd

# 运行 Docker 并挂载数据目录,映射卷
docker run \
    --name=dalistd \
    --restart always -d \
    -p 8090:80  \
    -v [存放学生图片的目录]:/FlaskAPP/app/static/std/101450/ \
    -v dalistdAPP:/FlaskAPP/app/templates/ \
    registry.cn-guangzhou.aliyuncs.com/danistd/danistd
```

## 镜像通过 Docker 实时构建
[URL](https://cr.console.aliyun.com/repository/cn-hangzhou/danistd/danistd/details)

