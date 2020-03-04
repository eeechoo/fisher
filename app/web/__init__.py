from flask import Blueprint, render_template

web = Blueprint('web', __name__, template_folder='templates')


@web.app_errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


@web.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


from app.web import auth
from app.web import main
from app.web import book
from app.web import wish
from app.web import gift
from app.web import drift
