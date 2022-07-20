import uuid
from datetime import date, timedelta
from flask import Blueprint, request
from blackbox import do_transaction
from payments_handler import do_loan_handler, pay_now_handler

# Constants

routes = Blueprint('routes', __name__)


@routes.route('/do_loan', methods=['POST'])
def do_loan():
    return do_loan_handler()


@routes.route('/pay_now', methods=['POST'])
def pay_now():
    return pay_now_handler()


