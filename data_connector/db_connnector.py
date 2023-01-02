import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

import db.model
from data_connector.connector import Connector
import settings
import pandas as pd


class DBConnector(Connector):

    def __init__(self, model):
        super().__init__(model)

    def __enter__(self):
        self.session = settings.session()

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @property
    def tablename(self):
        return self.model.__tablename__

    def get_daily_data(self, symbols=None, date=None, count=None):
        session = settings.session()

        query = self.model.query
        if symbols is not None and len(symbols) != 0:
            query = query.filter(self.model.Symbol.in_(symbols))

        if date is not None:
            query = query.filter(self.model.Date > date)

        df = pd.read_sql(query.statement, session.bind, index_col='Date')
        df = df.drop('Id', axis=1)
        return df

    def setup(self):
        from db.model import Base
        Base.metadata.create_all(bind=settings.Engine)

    def store_data(self, df):

        df.to_sql(
            self.tablename,
            settings.Engine,
            index=True,
            method="multi",
            chunksize=5000,
            if_exists='append')


if __name__ == '__main__':
    dom_stock_rate = db.model.DomStockRate()
    count = dom_stock_rate.query.count()
    print(count)
