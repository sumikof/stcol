from logging import getLogger
import pandas as pd

import yfinance as yf

logger = getLogger(__name__)


class YFinanceManager:
    filenm = ""

    def __init__(self):
        self.df = None

    @staticmethod
    def _download_rate_to_df(meig):
        logger.info(f'Download DailyRate Symbol From:{meig[0]} To:{meig[-1]}')
        rate_data = yf.download(meig, period='7d', interval="1d", group_by='ticker', )

        if rate_data.index.name is None:
            rate_data.index.name = 'DateTime'
        rate_data = rate_data.reset_index()
        rate_data['Date'] = rate_data['Date'].dt.strftime('%Y%m%d')
        rate_data = rate_data.set_index('Date')

        logger.info("finish download rate")
        if len(meig) > 1:
            return YFinanceManager._data_frame_convert(pd.DataFrame(rate_data))
        else:
            df = rate_data
            df['Symbol'] = meig[0]
            df['AdjClose'] = df['Adj Close']
            df = df.drop('Adj Close', axis=1)
        return df

    @staticmethod
    def _data_frame_convert(df):
        logger.info("dataframe convert start")
        df = df.stack(level=0)
        df = df.reset_index()
        df = df.set_axis(['Date', 'Symbol', 'AdjClose', 'Close', 'High', 'Low', 'Open', 'Volume'],
                         axis='columns')
        df = df.set_index('Date')
        logger.info("dataframe converted")
        return df

    def download_rate_from_symbols(self, symbols):
        meig = [i.value for i in symbols]
        if len(meig) > 1000:
            n = 500
            tmp_df = pd.DataFrame()
            for i in range(0, len(meig), n):
                tmp_df = pd.concat([tmp_df, self._download_rate_to_df(meig[i:i + n])])
            return tmp_df
        else:
            self.df = self._download_rate_to_df(meig)
        return self.df


def download_rate(symbols, model, data_connector):
    man = YFinanceManager()

    df = man.download_rate_from_symbols(symbols)
    # df = man.download_rate_from_symbols([symbol.Stock(8411),symbol.Stock(2503)])

    # already = con.get_daily_data(model=settings.DOM_STOCK_DATA, date='2021-01-01')

    # df = df.set_index('Symbol', append=True)
    # df = df.loc[df.index.difference(already.set_index('Symbol', append=True).index)].reset_index('Symbol')
    print(df)

    data_connector.store_data(df, model)

    # df = con.get_daily_data(settings.DOM_STOCK_DATA, symbols=[symbol.Stock(8411)], date='>20220302')
    # df = con.get_daily_data(settings.DOM_STOCK_DATA, date='20210802')

    print("finish store")

    # dm.upload_dataframe(dataframe=man.df, key=settings.DOM_STOCK_DATA)

    # df = dm.download_datafile(settings.DOM_STOCK_DATA)
    # print(df.head())


if __name__ == '__main__':
    from logging import INFO, basicConfig, DEBUG

    from stcol import data_connector
    import market.symbol
    import settings

    basicConfig(level=INFO, format=settings.LOG_FORMAT)
    logger.setLevel(DEBUG)
    # connector = data_connector.DBConncector()
    connector = data_connector.FileConnector()
    download_rate(market.symbol.DomStock, settings.DOM_STOCK_DATA, connector)
