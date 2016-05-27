#!/usr/bin/env python
# coding:utf-8
from flask import Flask, redirect, url_for, escape, request
from scheduler import insert
import json

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"


@app.route("/favicon.ico")
def favicon():
    return ""


@app.route("/sms_sender")
def sms():
    result = insert("SMSSenderWorker")
    out = []
    for v in result:
        out.append(v.get_id())
    return json.dumps(out)


@app.route("/push_worker", methods=['GET', 'POST'])
def push_worker():
    result = insert("PushWorker")
    out = []
    for v in result:
        out.append(v.get_id())
    return json.dumps(out)
    """
    if request.method == 'POST':
        return "PushWorker"
    else:
        return "PushWorker"
    """


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
