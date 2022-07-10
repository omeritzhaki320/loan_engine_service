import uuid
import csv
from datetime import date, timedelta
from blackbox import do_transaction
from models import Payments, Loans, PaymentStatus, PaymentType
from routes import SRC_BANK_ACCOUNT
from server import db, logger
from sqlalchemy import desc

# Constants
NOW = str(date.today() + timedelta(days=7))


def delay_payment(payment, loan_id):
    last_debit = Payments.query.filter_by(loan_id=loan_id).order_by(desc(Payments.due_date)).limit(1).first()
    new_debit = last_debit.due_date + timedelta(weeks=1)
    delay = Payments(id=uuid.uuid4().hex, loan_id=loan_id, transaction_id=None, amount=payment.amount,
                     status=PaymentStatus.PENDING, direction=PaymentType.DEBIT, due_date=new_debit)
    db.session.add(delay)
    logger.info(f"New payment date added to debit/s: {loan_id}")


def download_report():
    columns = ['Transaction ID', 'Loan ID', 'Due Date', 'Direction', 'Status']
    with open(f'{NOW}.csv', 'w', newline="") as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        for i in Payments.query.filter_by(due_date=NOW):
            payment = i.transaction_id, i.loan_id, i.due_date, i.direction, i.status
            writer.writerow(payment)
        logger.info(f"A daily report is created {NOW}")


def collector():
    payments = Payments.query.filter_by(due_date=NOW)
    for payment in payments:
        loan = Loans.query.filter_by(id=payment.loan_id).first()
        try:
            payment.transaction_id = do_transaction(src_bank=loan.account, dst_bank=SRC_BANK_ACCOUNT,
                                                    amount=payment.amount, direction=payment.direction)
            payment.status = PaymentStatus.SUCCEEDED
            loan.weeks_payed += 1
            logger.info(f"Payments were successfully collected")
        except Exception as e:
            print(str(e))
            payment.status = PaymentStatus.FAILED
            payment.transaction_id = None
            delay_payment(payment=payment, loan_id=loan.id)
            logger.info(f"The payment failed{payment.loan_id}")
        finally:
            db.session.commit()
    download_report()


if __name__ == '__main__':
    collector()
