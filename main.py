from flask import Flask, request, Response
import requests

app = Flask(__name__)

TARGET_HOST = "movie.douban.com"
TARGET_SCHEME = "https"
BASE_PATH = "/douban"

# 健康检查
@app.route("/healthy")
def hello_world():
    return "this working !"


# 监听根目录
@app.route(f"{BASE_PATH}/", defaults={"path": ""})
# 监听所有下级目录
@app.route(f"{BASE_PATH}/<path:path>")
def reverse_proxy(path):  # 这个变量其实不用，但必须要，不然会报错
    # 传递请求头
    headers = {k: v for k, v in request.headers if k.lower() != "host"}
    headers.update({"Host": TARGET_HOST})
    headers.update({"Accept-Encoding": "gzip, deflate"})
    # 重写请求URL
    url = (
        request.url.replace(request.host, TARGET_HOST)
        .replace(request.scheme, TARGET_SCHEME)
        .replace(BASE_PATH, "")
    )
    # 发送请求
    res = requests.request(
        method=request.method,
        url=url,
        headers=headers,
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False,
    )

    # 重写响应请求，需要去除一些与连接相关的头
    excluded_headers = [
        "content-encoding",
        "content-length",
        "transfer-encoding",
        "connection",
    ]
    headers = [
        (name, value)
        for (name, value) in res.raw.headers.items()
        if name.lower() not in excluded_headers
    ]

    # 修改一些内容
    if path.startswith("subject/4811774"):
        resp = res.text.replace("8.0", "0.8")
        # 返回响应
        return Response(resp, res.status_code, headers)
    # 返回响应
    return Response(res.content, res.status_code, headers)
