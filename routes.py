import csv
import uuid
from datetime import date, timedelta
from flask import Blueprint, request
from blackbox import do_transaction

# Constants
routes = Blueprint('routes', __name__)
SRC_BANK_ACCOUNT = 'my_bank'
NUMBER_OF_DEBIT_PAYMENTS = 12
NOW = date.today()


@routes.route('/do_loan', methods=['POST'])
def do_loan():
    from models import Loans, Payments, PaymentStatus, PaymentType
    from server import db, logger
    start_date = date.today()
    day_delta = timedelta(days=7)
    body = request.json
    transaction_id = do_transaction(SRC_BANK_ACCOUNT, body['dst_bank_account'], body['amount'], PaymentType.CREDIT)
    # Insert the Loan details to the db
    new_loan = Loans(id=uuid.uuid4().hex, transaction_id=transaction_id, amount=body['amount'],
                     account=body['dst_bank_account'], weeks_payed=0, start_date=start_date)
    db.session.add(new_loan)
    logger.info(f"A new loan has been created. Loan ID: {new_loan.id}")
    # Insert the Payments details to the db
    new_payment = Payments(id=uuid.uuid4().hex, loan_id=new_loan.id, transaction_id=transaction_id,
                           amount=body['amount'], status=PaymentStatus.SUCCEEDED, direction=PaymentType.CREDIT,
                           due_date=start_date)
    db.session.add(new_payment)
    per_debit = divide_amount(body['amount'])
    # Create the debits
    for week in range(1, 13):
        next_debit = start_date + (week * day_delta)
        debits_rows = Payments(id=uuid.uuid4().hex, loan_id=new_loan.id, transaction_id=None, amount=per_debit,
                               status=PaymentStatus.PENDING, direction=PaymentType.DEBIT, due_date=next_debit)
        db.session.add(debits_rows)
    logger.info(f"The loan was divided into 12 weeks.Loan ID: {new_loan.id}")
    db.session.commit()
    return "Transaction Succeeded"


@routes.route('/pay_now', methods=['POST'])
def pay_now():
    from models import Loans, Payments, PaymentStatus, PaymentType
    from server import db
    body = request.json
    payments = Payments.query.filter_by(status=PaymentStatus.PENDING, loan_id=body['loan_id']).all()
    left_to_pay = sum([payment.amount for payment in payments])
    for payment in payments:
        loan = Loans.query.filter_by(id=payment.loan_id).first()
        try:
            transaction_id = do_transaction(src_bank=loan.account, dst_bank=SRC_BANK_ACCOUNT,
                                            amount=left_to_pay, direction=PaymentType.DEBIT)
            new_payment = Payments(id=uuid.uuid4().hex, loan_id=body['loan_id'], transaction_id=transaction_id,
                                   amount=left_to_pay, status=PaymentStatus.SUCCEEDED, direction=PaymentType.DEBIT,
                                   due_date=NOW)
            db.session.add(new_payment)
            loan.weeks_payed += 1
            debits = Payments.query.filter_by(status=PaymentStatus.PENDING, loan_id=body['loan_id']).all()
            for debit in debits:
                debit.status = PaymentStatus.CANCELED
                download_report()
            db.session.commit()
        except Exception as e:
            print(str(e))
        finally:
            return 'test'


def download_report():
    from models import Payments
    columns = ['Transaction ID', 'Loan ID', 'Due Date', 'Amount', 'Direction', 'Status']
    with open(f'Pay Now - {NOW}.csv', 'w', newline="") as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        for i in Payments.query.filter_by(due_date=NOW):
            payment = i.transaction_id, i.loan_id, i.due_date,i.amount, i.direction, i.status
            writer.writerow(payment)
        # logger.info(f"A daily report is created {NOW}")


def divide_amount(amount):
    weekly_debit = amount / NUMBER_OF_DEBIT_PAYMENTS
    return weekly_debit
