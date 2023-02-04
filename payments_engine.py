import uuid
from datetime import date, timedelta

from flask import request

from processor import do_transaction

SRC_BANK_ACCOUNT = 'my_bank'
NUMBER_OF_DEBIT_PAYMENTS = 12
NOW = date.today()


def do_loan_handler():
    from db_models import Loans, Payments, PaymentStatus, PaymentType
    from app import db

    start_date = date.today()
    day_delta = timedelta(days=7)
    body = request.json
    transaction_id = do_transaction(SRC_BANK_ACCOUNT, body['dst_bank_account'], body['amount'], PaymentType.CREDIT)

    # Insert the Loan details to the db
    new_loan = Loans(id=uuid.uuid4().hex, transaction_id=transaction_id, amount=body['amount'],
                     account=body['dst_bank_account'], weeks_payed=0, start_date=start_date)
    db.session.add(new_loan)

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
    db.session.commit()
    return "Transaction Succeeded"


def pay_now_handler():
    from db_models import Loans, Payments, PaymentStatus, PaymentType
    from app import db

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
                debit.status = PaymentStatus.CANCELLED
            db.session.commit()
        except Exception as e:
            print(str(e))


def divide_amount(amount):
    weekly_debit = amount / NUMBER_OF_DEBIT_PAYMENTS
    return weekly_debit
