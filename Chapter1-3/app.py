#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'swl'
__mtime__ = '8/3/18'
"""
from flask import Flask, request, current_app, render_template

from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime

import requests

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)


# @app.route('/')
# def index():
#     user_agent = request.headers.get('User-Agent')
#     return "<h1>Hello World!,User-Agent is %s</h1>" % user_agent
#
#
# @app.route('/user/<name>')
# def user(name):
#     return "<h1>Hello %s</h1>" % name

# @app.route('/')
# def index():
#     return render_template("index.html")


@app.route('/')
def index():
    return render_template("index.html",current_time=datetime.utcnow())


@app.route('/user/<name>')
def user(name):
    return render_template("user.html", name=name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500


if __name__ == '__main__':
    # app_ctx = app.app_context()
    # app_ctx.push()
    # print(current_app.name)
    # app_ctx.pop()
    # print(app.url_map)
    # req = requests.get("https://www.baidu.com/")
    # print(req.status_code)
    # content = req.content
    # with open("templates/baidu.html",'wb') as f:
    #     f.write(content)

    app.run(debug=True)
