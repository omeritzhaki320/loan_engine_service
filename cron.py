from datetime import date, timedelta
from models import Payments, Loans
from server import db

now = str(date.today() + timedelta(days=7))
db_due_date = Payments.query.all()


def collector():
    for i in db_due_date:
        if i.due_date == now:
            update_status = Payments.query.filter_by(due_date=i.due_date).first()
            update_status.status = 'SUCCEEDED'
            update_loan = Loans.query.filter_by(weeks_payed=0).first()
            update_loan.weeks_payed = Loans.weeks_payed + 1
            db.session.commit()


if __name__ == '__main__':
    collector()
