from datetime import date, timedelta
from blackbox import do_transaction
from models import Payments, Loans, PaymentStatus
from routes import SRC_BANK_ACCOUNT
from server import db


def delay_payment(payment, load_id):
    pass


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
            delay_payment(payment=payment, load_id=loan.id)
        finally:
            db.session.commit()


if __name__ == '__main__':
    collector()
