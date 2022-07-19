import uuid
import csv
from datetime import date, timedelta

# Constants
NOW = str(date.today() + timedelta(weeks=2))


def do_transaction(src_bank, dst_bank, amount, direction):
    return uuid.uuid4().hex


def download_report():
    rows = []
    with open('report.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            rows.append(row)
        return rows


if __name__ == '__main__':
    download_report()
