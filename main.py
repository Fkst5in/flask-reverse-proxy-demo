from flask import Flask, request, redirect, Response
import requests
import brotli

app = Flask(__name__)

TARGET_HOST = "movie.douban.com"
TARGET_SCHEME = "https"
BASE_PATH = "/douban"


@app.route("/healthy")
def hello_world():
    return "this working !"


@app.route(f"{BASE_PATH}/", defaults={"path": ""})
@app.route(f"{BASE_PATH}/<path:path>")
def reverse_proxy(path):  # 这个变量其实不用，但必须要，不然会报错

    headers = {k: v for k, v in request.headers if k.lower() != "host"}
    headers.update({"Host": TARGET_HOST})
    headers.update({"Accept-Encoding": "gzip, deflate"})

    url = (
        request.url.replace(request.host, TARGET_HOST)
        .replace(request.scheme, TARGET_SCHEME)
        .replace(BASE_PATH, "")
    )

    res = requests.request(
        method=request.method,
        url=url,
        headers=headers,
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False,
    )

    print(res.text)

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

    if path.startswith("subject/4811774"):
        resp = res.text.replace("8.0", "0.8")
        return Response(resp, res.status_code, headers)

    return Response(res.content, res.status_code, headers)
