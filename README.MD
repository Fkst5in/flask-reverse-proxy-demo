# Flask 反向代理Demo
| flask + requests 做反向代理并修改响应内容

## 使用

克隆仓库
```
$ git clone https://github.com/Fkst5in/flask-reverse-proxy-demo && cd flask-reverse-proxy-demo
```
配置虚拟环境(可选)
```
$ python -m venv .venv
$ source .venv/bin/activate
```
安装依赖
```
$ pip install -r requirements.txt
```
运行
```
$ flask --app main run
```
检查
```
$ curl 127.0.0.1:5000/healthy
this working !
```