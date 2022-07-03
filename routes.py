import uuid
from datetime import datetime
from flask import Blueprint, request
from blackbox import do_transaction

routes = Blueprint('routes', __name__)
SRC_BANK_ACCOUNT = 'my_bank'


@routes.route('/do_loan', methods=['POST'])
def do_loan():
    from models import Loans, Payments, Debit
    from server import db
    now = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    due_date = datetime.now().strftime("%A")
    body = request.json
    transaction_id = do_transaction(SRC_BANK_ACCOUNT, body['dst_bank_account'], body['amount'], 'credit')
    # Insert the Loan details to the db
    new_loan = Loans(loan_id=uuid.uuid4().hex, account_id=body['dst_bank_account'], loan_sum=body['amount'],
                     weeks_payed=0, loan_start_date=now)
    db.session.add(new_loan)
    # Insert the Payments details to the db
    new_payment = Payments(transaction_id=transaction_id, loan_id=new_loan.loan_id, payment_sum=body['amount'],
                           is_payment_valid=True, payment_type='credit')
    db.session.add(new_payment)
    # Insert the Debits details to the db
    new_debit = Debit(debit_id=uuid.uuid4().hex, payment_id=uuid.uuid4().hex, loan_id=new_loan.loan_id,
                      due_date=due_date, status='PENDING')
    db.session.add(new_debit)
    db.session.commit()
    return "test"


def divide_amount():
    pass
