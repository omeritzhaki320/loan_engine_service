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
    id = db.Column(db.String(70), unique=True, nullable=False, primary_key=True)
    transaction_id = db.Column(db.String(70), unique=True, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    account = db.Column(db.String(70), unique=True, nullable=False)
    weeks_payed = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.String(50), nullable=False)


class Payments(db.Model):
    id = db.Column(db.String(70), unique=True, nullable=False, primary_key=True)
    loan_id = db.Column(db.String(70), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.Enum(DebitStatus), nullable=False)
    direction = db.Column(db.Enum(PaymentType), nullable=False)
    due_date = db.Column(db.String(50), nullable=False)





