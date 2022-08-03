import uuid
from datetime import date, timedelta
from blackbox import do_transaction, download_report
from models import Payments, Loans, PaymentStatus, PaymentType
from payments_handler import SRC_BANK_ACCOUNT
from server import db, logger
from sqlalchemy import desc

# Constants
NOW = str(date.today() + timedelta(weeks=2))


def delay_payment(payment, loan_id):
    last_debit = Payments.query.filter_by(loan_id=loan_id).order_by(desc(Payments.due_date)).limit(1).first()
    new_debit = last_debit.due_date + timedelta(weeks=1)
    delay = Payments(id=uuid.uuid4().hex, loan_id=loan_id, transaction_id=None, amount=payment.amount,
                     status=PaymentStatus.PENDING, direction=PaymentType.DEBIT, due_date=new_debit)
    db.session.add(delay)
    logger.info(f"New payment date added to debit/s: {loan_id}")


def collector():
    payments = Payments.query.filter_by(due_date=NOW)
    for payment in payments:
        loan = Loans.query.filter_by(id=payment.loan_id).one()
        payment.transaction_id = do_transaction(src_bank=loan.account, dst_bank=SRC_BANK_ACCOUNT,
                                                amount=payment.amount, direction=payment.direction)
        payment.status = PaymentStatus.PENDING
    for i in download_report():
        p = Payments.query.filter_by(transaction_id=i[0]).one()
        p.status = i[1]
        if i[1] == PaymentStatus.SUCCEEDED:
            loan = Loans.query.filter_by(id=p.loan_id).first()
            loan.weeks_payed += 1
        elif i[1] == PaymentStatus.FAILED:
            delay_payment(payment=p, loan_id=p.loan_id)
    db.session.commit()


if __name__ == '__main__':
    collector()
