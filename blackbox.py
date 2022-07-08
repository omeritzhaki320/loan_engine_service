import random
import uuid


def do_transaction(src_bank, dst_bank, amount, direction):
    if direction != 'CREDIT' and random.randint(1, 10) > 8:
        raise Exception("Transaction failed")
    return uuid.uuid4().hex
