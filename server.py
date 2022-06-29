import uuid
import local_secrets
import models
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from blackbox import do_transaction

# CONSTANTS
SRC_BANK_ACCOUNT = 'my_bank'
HOST = local_secrets.host
USER = local_secrets.user
PASSWD = local_secrets.passwd
DATABASE = local_secrets.database

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + USER + ':' + PASSWD + '@' + HOST + '/' + DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


@app.route('/do_loan', methods=['POST'])
def do_loan():
    from models import Loans, Payments
    now = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    body = request.json
    transaction_id = do_transaction(SRC_BANK_ACCOUNT, body['dst_bank_account'], body['amount'], 'credit')
    loans_query = Loans(loan_id=uuid.uuid4().hex, account_id=body['dst_bank_account'], loan_sum=body['amount'],
                        weeks_payed=0, loan_start_date=now)

    payments_query = Payments(transaction_id=transaction_id, loan_id=loans_query.loan_id, payment_sum=body['amount'],
                              is_payment_valid=True, payment_type='credit')

    db.session.add(loans_query)
    db.session.add(payments_query)
    db.session.commit()
    weekly_debits(body['amount'], loans_query.loan_start_date, body['dst_bank_account'])
    return transaction_id


def weekly_debits(amount, start_date, dst_bank):
    weekly_payments = amount / 12


if __name__ == '__main__':
    models.db.create_all()
    app.run(debug=True)