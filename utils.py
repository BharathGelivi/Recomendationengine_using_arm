from datetime import datetime
def timestamp():
    return datetime.now().strftime('%Y%m%d_%H%M%S')

def read_transactions_csv(path):
    transactions = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            cleaned = line.strip()
            if cleaned:
                items = [x.strip() for x in cleaned.split(',') if x.strip()]
                transactions.append(items)
    return transactions
