from stcol.data_connector import FileConnector


class RateService:
    def __init__(self):
        self.connector = FileConnector()

    def daily_rate(self,
                   model,
                   symbols=None,
                   date=None,
                   count=0):
        df = self.connector.get_daily_data(
            model=model,
            symbols=symbols,
            date=date,
            count=count)

        df = df.reset_index().set_index(["Symbol", 'Date'])

        item = {
            symbol:
            {
                "symbol": symbol,
                "rates": df.loc[symbol].to_dict(orient='index')
            }
            for symbol in df.index.get_level_values('Symbol').unique()
        }

        return item
