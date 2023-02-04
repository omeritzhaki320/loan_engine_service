from enum import Enum

from app import db


class PaymentType(str, Enum):
    DEBIT = 'DEBIT'
    CREDIT = 'CREDIT'


class PaymentStatus(str, Enum):
    PENDING = 'PENDING'
    SUCCEEDED = 'SUCCEEDED'
    FAILED = 'FAILED'
    CANCELLED = 'CANCELLED'


class Loans(db.Model):
    id = db.Column(db.String(70), unique=True, nullable=False, primary_key=True)
    transaction_id = db.Column(db.String(70), unique=True, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    account = db.Column(db.String(70), unique=False, nullable=False)
    weeks_payed = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)


class Payments(db.Model):
    id = db.Column(db.String(70), unique=True, nullable=False, primary_key=True)
    loan_id = db.Column(db.String(70), nullable=False)
    transaction_id = db.Column(db.String(70), unique=True, nullable=True)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.Enum(PaymentStatus), nullable=False)
    direction = db.Column(db.Enum(PaymentType), nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
