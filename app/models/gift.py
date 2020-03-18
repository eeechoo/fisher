from collections import defaultdict

from flask import current_app
from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, desc, func
from sqlalchemy.orm import relationship

from app.helpers.spider.yushu_book import YuShuBook
from app.models.base import Base, db
from app.models.wish import Wish
from app.viewmodels.book import BookViewModel


class Gift(Base):
    __tablename__ = 'gift'

    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey('user.id'), nullable=False)
    isbn = Column(String(13))
    launched = Column(Boolean, default=False)

    user = relationship('User')

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first

    @staticmethod
    def recent():
        gift_list = Gift.query.filter_by(launched=False).order_by(
            desc(Gift.create_time)).limit(
            current_app.config['RECENT_BOOK_PER_PAGE']).all()
        books = [BookViewModel(gift.book) for gift in gift_list]
        return books

    @staticmethod
    def get_wish_counts(gifts):
        book_isbn_list = [gift.isbn for gift in gifts]

        ret = defaultdict(int)
        temp_list = db.session.query(
            func.count(Wish.id), Wish.isbn).filter(
            Wish.launched == False, Wish.isbn.in_(book_isbn_list), Wish.status == 1).group_by(
            Wish.isbn).all()
        for temp in temp_list:
            ret[temp[1]] = temp[0]

        return ret

    def is_yourself_gift(self, uid):
        return uid == self.uid
