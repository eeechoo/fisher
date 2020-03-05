from flask import current_app, flash, redirect, url_for
from flask_login import login_required, current_user

from . import web
from .. import db
from ..models.gift import Gift


@web.route('/my/gifts')
@login_required
def my_gifts():
    pass


@web.route('/gifts/book/<isbn>')
def save_to_gifts(isbn):
    if current_user.can_save_to_list(isbn):
        # 既不在赠送清单，也不在心愿清单才能添加
        with db.auto_commit():
            gift = Gift()
            gift.uid = current_user.id
            gift.isbn = isbn
            # gift.book_id = yushu_book.data.id
            db.session.add(gift)
            current_user.beans += current_app.config['BEANS_UPLOAD_ONE_BOOK']
    else:
        flash('这本书已添加至你的赠送清单或已存在于你的心愿清单，请不要重复添加')
    return redirect(url_for('web.book_detail', isbn=isbn))


@web.route('/gifts/<gid>/redraw')
def redraw_from_gifts(gid):
    pass
