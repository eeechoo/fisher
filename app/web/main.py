from flask import render_template

from . import web


__author__ = '七月'


@web.route('/')
def index():
    return render_template('index.html', recent=[])


@web.route('/personal')
def personal_center():
    pass
