#!/usr/bin/env python
# coding:utf-8
try:
    from gevent import monkey
    from gevent.wsgi import WSGIServer

    monkey.patch_all()
    run_on_stardand_mode = False
except ImportError:
    run_on_stardand_mode = True
    pass

from flask import Flask, redirect, url_for, escape, request
from lib.units import scan_worker
from scheduler import insert
import json

app = Flask(__name__)


@app.route("/")
def hello():
    worker_list = scan_worker("./conf", ext=".conf")
    out = []
    for worker in worker_list:
        out.append("http://%s:%d/%s" % (app.host, app.port, worker.lower()))
    return json.dumps(out)


@app.route("/favicon.ico")
def favicon():
    return ""


@app.route("/smsworker")
def sms():
    result = insert("SMSWorker")
    out = []
    for v in result:
        out.append(v.get_id())
    return json.dumps(out)


@app.route("/pushworker", methods=['GET', 'POST'])
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
    app.host = "0.0.0.0"
    app.port = 5000
    if run_on_stardand_mode is False:
        print "Run on gevent.wsgi at http://%s:%d" % (app.host, app.port)
        http_server = WSGIServer((app.host, app.port), app)
        http_server.serve_forever()
    else:
        print "Run on flask stardand at http://%s:%d" % (app.host, app.port)
        app.run(host='0.0.0.0')
