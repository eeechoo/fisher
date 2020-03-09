from sqlalchemy import desc

from app.models.gift import Gift
from app.viewmodels.book import BookViewModel


class MyGifts:
    def __init__(self, uid):
        self.gifts = []

        # self 绑定的数据不建议直接修改，而是应该通过函数修改后，赋值
        self.gifts = self._fill(uid)

    def _fill(self, uid):
        gifts = Gift.query.filter_by(
            uid=uid, launched=False).order_by(
            desc(Gift.create_time)).all()
        bookisbn_to_wants_map = Gift.get_wish_counts(gifts)
        return [{
            'wishes_count': bookisbn_to_wants_map[gift.isbn],
            'book': BookViewModel(gift.book),
            'id': gift.id}
            for gift in gifts]
