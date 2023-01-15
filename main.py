from flask import Flask

app = Flask(__name__)


@app.route("/healthy")
def hello_world():
    return "OK"


@app.rouote("/headers", methods=["GET", "POST"])
def return_headers():
    return "fine"
