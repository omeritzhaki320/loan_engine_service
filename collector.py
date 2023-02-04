import uuid
from datetime import date, timedelta

from sqlalchemy import desc

from processor import do_transaction, download_report
from db_models import Payments, Loans, PaymentStatus, PaymentType
from payments_engine import SRC_BANK_ACCOUNT
from app import db

NOW = str(date.today() + timedelta(weeks=2))


def delay_payment(payment, loan_id):
    """
      Creates a new delayed payment
      :param payment: the payment to be delayed
      :param loan_id: the loan id
      :return: the new delayed payment
      """
    last_debit = Payments.query.filter_by(loan_id=loan_id).order_by(desc(Payments.due_date)).limit(1).first()
    new_debit = last_debit.due_date + timedelta(weeks=5)
    delay = Payments(id=uuid.uuid4().hex, loan_id=loan_id, transaction_id=None, amount=payment.amount,
                     status=PaymentStatus.PENDING, direction=PaymentType.DEBIT, due_date=new_debit)
    db.session.add(delay)


def collect_debits():
    """
    The main function that handles payments and loans
    """
    payments_due = Payments.query.filter_by(due_date=NOW)
    for payment in payments_due:
        associated_loan = Loans.query.filter_by(id=payment.loan_id).one()
        payment.transaction_id = do_transaction(src_bank=associated_loan.account, dst_bank=SRC_BANK_ACCOUNT,
                                                amount=payment.amount, direction=payment.direction)
        payment.status = PaymentStatus.PENDING
    for transaction_report in download_report():
        associated_payment = Payments.query.filter_by(transaction_id=transaction_report[0]).one()
        associated_payment.status = transaction_report[1]
        if transaction_report[1] == PaymentStatus.SUCCEEDED:
            associated_loan = Loans.query.filter_by(id=associated_payment.loan_id).first()
            associated_loan.weeks_payed += 1
        elif transaction_report[1] == PaymentStatus.FAILED:
            delay_payment(payment=associated_payment, loan_id=associated_payment.loan_id)
    db.session.commit()


if __name__ == '__main__':
    collect_debits()
