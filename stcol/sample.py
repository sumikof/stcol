from stcol.db.model import DomStockRate


def main():
    num = DomStockRate.query.first().Symbol
    print(num)
