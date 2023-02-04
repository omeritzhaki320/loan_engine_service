from flask import Blueprint

from payments_engine import do_loan_handler, pay_now_handler

routes = Blueprint('routes', __name__)


@routes.route('/do_loan', methods=['POST'])
def do_loan():
    return do_loan_handler()


@routes.route('/pay_now', methods=['POST'])
def pay_now():
    return pay_now_handler()
