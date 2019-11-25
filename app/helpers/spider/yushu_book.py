from app.helpers.libs.http import Http


class YuShuBook:
    """
        鱼书API提供数据
    """
    per_page = 15
    # 豆瓣开发者平台已经不再提供豆瓣 API 接口
    # isbn_url = 'https://api.douban.com/v2/book/isbn/{}'
    # keyword_url = 'https://api.douban.com/v2/book/search?q={}&count={}&start={}'
    isbn_url = 'http://t.yushu.im/v2/book/isbn/{}'
    keyword_url = 'http://t.yushu.im/v2/book/search?q={}&count={}&start={}'

    def __init__(self):
        """
        data 有三种情况：
            1. 空
            2. 单本
            3. 有多个结果
        我们要将获得的三种情况统一起来
        """
        self.total = 0
        self.books = []

    def search_by_isbn(self, isbn):
        url = self.isbn_url.format(isbn)
        result = Http.get(url)
        self.__fill_single(result)

    def search_by_keyword(self, keyword, page):
        page = int(page)
        url = self.keyword_url.format(keyword, self.per_page, self.per_page * (page - 1))
        result = Http.get(url)
        self.__fill_collection(result)

    def __fill_single(self, data):
        if data:
            self.total = 1
            self.books.append(data)

    def __fill_collection(self, data):
        self.total = data['total']
        self.books = data['books']

    @property
    def first(self):
        return self.books[0] if self.total >= 1 else None
