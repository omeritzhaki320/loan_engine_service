# # engine = sqlalchemy.create_engine('mysql+pymysql://' + USER + ':' + PASSWD + '@' + HOST + '/' + DATABASE)
# # engine.execute("CREATE SCHEMA IF NOT EXISTS `Loans`;")
# # engine.execute("USE Loans;")
#
# import uuid
# from enum import Enum
# import local_secrets
# from flask import Flask, request
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime
# from blackbox import do_transaction
#
# # CONSTANTS
# SRC_BANK_ACCOUNT = 'my_bank'
# HOST = local_secrets.host
# USER = local_secrets.user
# PASSWD = local_secrets.passwd
# DATABASE = local_secrets.database
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + USER + ':' + PASSWD + '@' + HOST + '/' + DATABASE
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#
# db = SQLAlchemy(app)
#
#
# class PaymentType(str, Enum):
#     DEBIT = 'DEBIT'
#     CREDIT = 'CREDIT'
#
#
# class Loans(db.Model):
#     loan_id = db.Column(db.String(70), unique=True, nullable=False, primary_key=True)
#     account_id = db.Column(db.String(70), unique=True, nullable=False)
#     loan_sum = db.Column(db.Integer, nullable=False)
#     weeks_payed = db.Column(db.Integer, nullable=False)
#     loan_start_date = db.Column(db.String(50), nullable=False)
#
#
# class DstBankAccount(db.Model):
#     account_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
#     account_number = db.Column(db.Integer, nullable=False)
#     dst_bank = db.Column(db.String(50), unique=True, nullable=False)
#
#
# class Payments(db.Model):
#     transaction_id = db.Column(db.String(70), unique=True, nullable=False, primary_key=True)
#     loan_id = db.Column(db.String(70), nullable=False)
#     payment_sum = db.Column(db.Integer, nullable=False)
#     is_payment_valid = db.Column(db.Boolean, nullable=False)
#     payment_type = db.Column(db.Enum(PaymentType), nullable=False)
#
#
# @app.route('/do_loan', methods=['POST'])
# def do_loan():
#     # from models import Loans, Payments
#     now = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
#     body = request.json
#     transaction_id = do_transaction(SRC_BANK_ACCOUNT, body['dst_bank_account'], body['amount'], 'credit')
#     loans_query = Loans(loan_id=uuid.uuid4().hex, account_id=body['dst_bank_account'], loan_sum=body['amount'],
#                         weeks_payed=0, loan_start_date=now)
#
#     payments_query = Payments(transaction_id=transaction_id, loan_id=loans_query.loan_id, payment_sum=body['amount'],
#                               is_payment_valid=True, payment_type='credit')
#
#     db.session.add(loans_query)
#     db.session.add(payments_query)
#     db.session.commit()
#     weekly_debits(body['amount'], loans_query.loan_start_date, body['dst_bank_account'])
#     return transaction_id
#
#
# def weekly_debits(amount, start_date, dst_bank):
#     weekly_payments = amount / 12
#
#
# if __name__ == '__main__':
#     db.create_all()
#     app.run(debug=True)
