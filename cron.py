from datetime import date, timedelta
from blackbox import do_transaction
from models import Payments, Loans, PaymentStatus
from routes import SRC_BANK_ACCOUNT
from server import db


def delay_payment(payment, loan_id):
    last_debit = date.today() + timedelta(weeks=12)
    payment = Payments.query.filter_by(status=PaymentStatus.FAILED)
    delay_debit = date.today() + timedelta(weeks=13)
    for i in payment:
        loan = Loans.query.filter_by(last_debit=last_debit)
        i.due_date = delay_debit
        loan.last_debit = delay_debit


def collector():
    now = str(date.today() + timedelta(days=7))
    payments = Payments.query.filter_by(due_date=now)
    for payment in payments:
        loan = Loans.query.filter_by(id=payment.loan_id).first()
        try:
            payment.transaction_id = do_transaction(src_bank=loan.account, dst_bank=SRC_BANK_ACCOUNT,
                                                    amount=payment.amount, direction=payment.direction)
            payment.status = PaymentStatus.SUCCEEDED
            loan.weeks_payed += 1
        except Exception as e:
            print(str(e))
            payment.status = PaymentStatus.FAILED
            payment.transaction_id = None
            delay_payment(payment=payment, loan_id=loan.id)
        finally:
            db.session.commit()


if __name__ == '__main__':
    collector()
