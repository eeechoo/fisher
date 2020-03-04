# 用于 session 加密
SECRET_KEY = '123'

# 用于 mysql
SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:@localhost/fisher'

# Email 配置
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TSL = False
# 密码这里如何填写 参考下面这两个链接
# https://service.mail.qq.com/cgi-bin/help?subtype=1&&no=1001256&&id=28
# https://blog.csdn.net/wbin233/article/details/73222027
# MAIL_USERNAME = 'hello@yushu.im'
# MAIL_PASSWORD = 'Bmwzy1314520'
# MAIL_SENDER = '鱼书 <hello@yushu.im>'
# 注意 MAIL_USERNAME 和 MAIL_SENDER 中使用的邮箱必须相同，qq邮箱才接受你这个发送请求
MAIL_USERNAME = 'xxxxxx@qq.com'
MAIL_PASSWORD = 'yyyyyy'
MAIL_SUBJECT_PREFIX = '[鱼书]'
MAIL_SENDER = '鱼书 <xxxxxx@qq.com>'





