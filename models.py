from enum import Enum
from server import db


class PaymentType(str, Enum):
    DEBIT = 'DEBIT'
    CREDIT = 'CREDIT'


class DebitStatus(str, Enum):
    PENDING = 'PENDING'
    SUCCEEDED = 'SUCCEEDED'
    FAILED = 'FAILED'


class Loans(db.Model):
    loan_id = db.Column(db.String(70), unique=True, nullable=False, primary_key=True)
    account_id = db.Column(db.String(70), unique=True, nullable=False)
    loan_sum = db.Column(db.Integer, nullable=False)
    weeks_payed = db.Column(db.Integer, nullable=False)
    loan_start_date = db.Column(db.String(50), nullable=False)


class Payments(db.Model):
    transaction_id = db.Column(db.String(70), unique=True, nullable=False, primary_key=True)
    loan_id = db.Column(db.String(70), nullable=False)
    payment_sum = db.Column(db.Integer, nullable=False)
    is_payment_valid = db.Column(db.Boolean, nullable=False)
    payment_type = db.Column(db.Enum(PaymentType), nullable=False)


class Debit(db.Model):
    debit_id = db.Column(db.String(70), nullable=False, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    payment_id = db.Column(db.String(70), nullable=True)
    loan_id = db.Column(db.String(70), nullable=False)
    due_date = db.Column(db.String(50), nullable=False)
    status = db.Column(db.Enum(DebitStatus), nullable=False)


