from models import Payments
from server import db

query = Payments(transaction_id=188234, loan_id=164623, payment_sum=12000, is_payment_valid=True, payment_type="DEBIT")
db.session.add(query)
db.session.commit()
