from flask import Flask
from flask_login import LoginManager

from app.models.base import db


login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # 配置
    # secure 代表秘密配置
    # settings 代表常规配置
    app.config.from_object('app.secure')
    app.config.from_object('app.settings')

    # 注册 SQLAlchemy
    db.init_app(app)
    # 创建 table 可以这样写
    # from app.models.user import User
    # with app.app_context():
    #     db.create_all()

    # 注册 flask-login
    login_manager.init_app(app)
    login_manager.login_view = 'web.login'
    login_manager.login_message = '请先登录或注册'

    register_blueprint(app)

    # 创建 table 也可以这样写，写在注册蓝图之后，因为注册蓝图时会执行到
    # class User(db.Model)，写这句的时候，会反作用到db，接下来db.create_all()的时候就会创建对应的表结构了
    with app.app_context():
        db.create_all()

    return app


def register_blueprint(app):
    from app.web import web
    app.register_blueprint(web)
