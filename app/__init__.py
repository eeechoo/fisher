from flask import Flask


def create_app():
    app = Flask(__name__)

    # 配置
    # secure 代表秘密配置
    # settings 代表常规配置
    app.config.from_object('app.secure')
    app.config.from_object('app.settings')

    register_blueprint(app)

    return app


def register_blueprint(app):
    from app.web import web
    app.register_blueprint(web)
