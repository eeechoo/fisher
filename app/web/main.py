from flask import render_template

from . import web
from ..models.gift import Gift


@web.route('/')
def index():
    gift_list = Gift.recent()
    return render_template('index.html', recent=gift_list)
