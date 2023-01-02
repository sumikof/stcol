from db.model import DomStockRate


def main():
    num = DomStockRate.query.first()
    print(num)
