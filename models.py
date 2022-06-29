from enum import Enum
from server import db


class PaymentType(str, Enum):
    DEBIT = 'DEBIT'
    CREDIT = 'CREDIT'


class Loans(db.Model):
    loan_id = db.Column(db.String(70), unique=True, nullable=False, primary_key=True)
    account_id = db.Column(db.String(70), unique=True, nullable=False)
    loan_sum = db.Column(db.Integer, nullable=False)
    weeks_payed = db.Column(db.Integer, nullable=False)
    loan_start_date = db.Column(db.String(50), nullable=False)


class DstBankAccount(db.Model):
    account_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    account_number = db.Column(db.Integer, nullable=False)
    dst_bank = db.Column(db.String(50), unique=True, nullable=False)


class Payments(db.Model):
    transaction_id = db.Column(db.String(70), unique=True, nullable=False, primary_key=True)
    loan_id = db.Column(db.String(70), nullable=False)
    payment_sum = db.Column(db.Integer, nullable=False)
    is_payment_valid = db.Column(db.Boolean, nullable=False)
    payment_type = db.Column(db.Enum(PaymentType), nullable=False)
