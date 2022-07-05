import uuid
from datetime import date, timedelta, datetime
from flask import Blueprint, request
from blackbox import do_transaction

# Constants
routes = Blueprint('routes', __name__)
SRC_BANK_ACCOUNT = 'my_bank'
NUMBER_OF_DEBIT_PAYMENTS = 12


@routes.route('/do_loan', methods=['POST'])
def do_loan():
    from models import Loans, Payments
    from server import db
    now = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    due_date = date.today()
    first_debit = due_date + timedelta(days=7)
    day_delta = timedelta(days=7)
    body = request.json
    transaction_id = do_transaction(SRC_BANK_ACCOUNT, body['dst_bank_account'], body['amount'], 'credit')
    # Insert the Loan details to the db
    new_loan = Loans(id=uuid.uuid4().hex, transaction_id=uuid.uuid4().hex, amount=body['amount'],
                     account=body['dst_bank_account'], weeks_payed=0, start_date=now)
    db.session.add(new_loan)
    # Insert the Payments details to the db
    new_payment = Payments(id=uuid.uuid4().hex, loan_id=new_loan.id, amount=body['amount'], status='SUCCEEDED', direction='CREDIT',
                           due_date=due_date)
    db.session.add(new_payment)
    per_debit = divide_amount(body['amount'])
    # Create the debits
    for week in range(NUMBER_OF_DEBIT_PAYMENTS):
        next_debit = first_debit + (week * day_delta)
        debits_rows = Payments(id=uuid.uuid4().hex, loan_id=new_loan.id, amount=per_debit, status='PENDING', direction='DEBIT',
                               due_date=next_debit)
        db.session.add(debits_rows)
    db.session.commit()
    return "test"


def divide_amount(amount):
    weekly_debit = amount / NUMBER_OF_DEBIT_PAYMENTS
    return weekly_debit
