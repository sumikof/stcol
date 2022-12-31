from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy import UniqueConstraint
from settings import Base,DATA_PATH


class TableBase:
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Date = Column(Text, index=True)
    Symbol = Column(String(30), index=True)
    Open = Column(Float)
    Close = Column(Float)
    High = Column(Float)
    Low = Column(Float)
    Volume = Column(Float)
    AdjClose = Column(Float)
    __table_args__ = (UniqueConstraint('Date', 'Symbol'), )


class FutureRate(Base,TableBase):
    __tablename__ = "FUTURE"
    filename = 'future.csv'


class IndexRate(Base,TableBase):
    __tablename__ = "INDEX"
    filename = 'index.csv'


class OvrEtfRate(Base,TableBase):
    __tablename__ = "OVR_ETF"
    filename = 'ovr_etf.csv'


class BondYieldsRate(Base,TableBase):
    __tablename__ = "BOND_YIELDS"
    filename = 'bond_yields.csv'


class ExchangeRate(Base,TableBase):
    __tablename__ = "EXCHANGE"
    filename = 'exchange.csv'


class DomStockRate(Base,TableBase):
    __tablename__ = "DOM_STOCK"
    filename = 'dom_stock.csv'

if __name__ == '__main__':
    dom_stock_rate = DomStockRate()
    count = dom_stock_rate.query.count()
    print(count)