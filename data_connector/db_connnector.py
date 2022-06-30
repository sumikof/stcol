import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from data_connector.connector import Connector
import db
import settings
import pandas as pd


class DBConncector(Connector):

    def get_daily_data(self, model, symbols=None,date=None):
        session = settings.make_session()
        model_type = type(model)

        query = session.query(model_type)
        if symbols is not None and len(symbols) != 0:
            query = query.filter(model_type.Symbol.in_(symbols))

        if date is not None:
            query = query.filter(model_type.Date > date)

        df = pd.read_sql(query.statement, session.bind, index_col='Date')
        df = df.drop('Id', axis=1)
        return df

    def setup(self):
        db.model.Base.metadata.create_all(bind=settings.Engine)

    def store_data(self, df, model):

        df.to_sql(
            model.__tablename__,
            settings.Engine,
            index=True,
            method="multi",
            chunksize=5000,
            if_exists='append')
