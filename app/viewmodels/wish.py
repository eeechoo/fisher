from sqlalchemy import desc

from app.models.wish import Wish
from app.viewmodels.book import BookViewModel


class MyWishes:
    def __init__(self, uid):
        self.wishes = []

        # self 绑定的数据不建议直接修改，而是应该通过函数修改后，赋值
        self.wishes = self._fill(uid)

    def _fill(self, uid):
        wishes = Wish.query.filter_by(
            uid=uid, launched=False).order_by(
            desc(Wish.create_time)).all()
        bookisbn_to_gives_map = Wish.get_gift_counts(wishes)
        return [{
            'wishes_count': bookisbn_to_gives_map[wish.isbn],
            'book': BookViewModel(wish.book),
            'id': wish.id}
            for wish in wishes]
