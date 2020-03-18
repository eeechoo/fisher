from flask import flash, redirect, url_for, request, render_template
from flask_login import login_required, current_user
from sqlalchemy import or_, desc

from . import web
from .. import db
from ..forms.book import DriftForm
from ..helpers.libs.email import send_email
from ..helpers.libs.enums import PendingStatus
from ..models.drift import Drift
from ..models.gift import Gift
from ..models.user import User
from ..models.wish import Wish
from ..viewmodels.book import BookViewModel
from ..viewmodels.drift import DriftCollection


@web.route('/drift/<int:gid>', methods=['GET', 'POST'])
@login_required
def send_drift(gid):
    current_gift = Gift.query.get_or_404(gid)
    if current_gift.is_yourself_gift(current_user.id):
        flash('这本书是自己的(*^▽^*)，不能向自己索要哦')
        return redirect(url_for('web.book_detail', isbn=current_gift.isbn))

    # 当前用户 beans 大于 1 且 当前用户需要满足每得到一本就送出两本 约束
    can = current_user.can_send_drifts()

    form = DriftForm(request.form)
    if request.method == 'POST' and form.validate():
        save_drift(form, current_gift)
        send_email(current_gift.user.email, '有人想要一本书', 'email/get_gift',
                   wisher=current_user,
                   gift=current_gift)
        return redirect(url_for('web.pending'))
    gifter = current_gift.user.summary
    return render_template('drift.html', gifter=gifter, user_beans=current_user.beans, form=form)


def save_drift(drift_form, current_gift):
    with db.auto_commit():
        drift = Drift()
        drift_form.populate_obj(drift)

        drift.gift_id = current_gift.id
        drift.requester_id = current_user.id
        drift.requester_nickname = current_user.nickname
        drift.gifter_nickname = current_gift.user.nickname
        drift.gifter_id = current_gift.user.id

        book = BookViewModel(current_gift.book)
        drift.book_title = book.title
        drift.book_author = book.author
        drift.book_img = book.image
        drift.isbn = book.isbn

        db.session.add(drift)

        current_user.beans -= 1


@web.route('/pending')
def pending():
    drifts = Drift.query.filter(
        or_(Drift.requester_id == current_user.id,
            Drift.gifter_id == current_user.id)) \
        .order_by(desc(Drift.create_time)).all()

    views = DriftCollection(drifts, current_user.id)
    return render_template('pending.html', drifts=views.data)


@web.route('/drift/<int:did>/reject')
@login_required
def reject_drift(did):
    with db.auto_commit():
        # requester_id=current_user.id 防止超权现象
        drift = Drift.query.filter_by(
            id=did, gifter_id=current_user.id).first_or_404()
        drift.pending = PendingStatus.Reject

        requester = User.query.get_or_404(drift.requester_id)
        requester.beans += 1

    return redirect(url_for('web.pending'))


@web.route('/drift/<int:did>/redraw')
@login_required
def redraw_drift(did):
    with db.auto_commit():
        # requester_id=current_user.id 防止超权现象
        drift = Drift.query.filter_by(
            id=did, requester_id=current_user.id).first_or_404()
        drift.pending = PendingStatus.Redraw
        current_user.beans += 1

    return redirect(url_for('web.pending'))


# 显然，这里的功能应该使用 ajax 实现
@web.route('/drift/<int:did>/mailed')
@login_required
def mailed_drift(did):
    with db.auto_commit():
        # 更改鱼漂状态位成功
        drift = Drift.query.filter_by(
            id=did, gifter_id=current_user.id).first_or_404()
        drift.pending = PendingStatus.Success

        # 赠送一个鱼豆
        current_user.beans += 1

        # 完成赠送
        gift = Gift.query.get_or_404(drift.gift_id)
        gift.launched = True
        # 完成心愿
        Wish.query.filter_by(
            isbn=drift.isbn, uid=drift.requester_id, launched=False) \
            .update({Wish.launched: True})

        current_user.send_counter += 1
        User.query.filter_by(id=drift.requester_id).receive_counter += 1

        return redirect(url_for('web.pending'))
