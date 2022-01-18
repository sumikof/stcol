from logging import getLogger
import os
import pandas as pd

import yfinance as yf

import edinet
import settings
import symbol

logger = getLogger(__name__)


class YFinanceManager:
    filenm = ""

    def __init__(self):
        self.df = None

    @staticmethod
    def _download_rate_to_df(meig):
        data = yf.download(meig, period='25y', interval="1d", group_by='ticker', )
        logger.info("finish download rate")
        df = YFinanceManager._data_frame_convert(pd.DataFrame(data))
        return df

    @staticmethod
    def _data_frame_convert(df):
        logger.info("dataframe convert start")
        df = df
        df = df.stack(level=0)
        df = df.reset_index()
        df = df.set_axis(['Date', 'Symbol', 'AdjClose', 'Close', 'High', 'Low', 'Open', 'Volume'],
                         axis='columns')
        df = df.set_index('Date')
        logger.info("dataframe converted")
        return df

    def download_rate_from_symbols(self, symbols):
        meig = [i.value for i in symbols]
        self.df = self._download_rate_to_df(meig)


class Stock(YFinanceManager):
    def __init__(self):
        self.df = None
        self.filenm = "dom_stock.csv"

    def download_stockrate(self, code_from, code_to):
        kabu_df = edinet.kabu()
        # 必要な列だけ抽出
        kabu_df = kabu_df.loc[:, ['ＥＤＩＮＥＴコード', edinet.COLS.CODE, '提出者名', '提出者業種', ]]

        code = kabu_df[edinet.COLS.CODE].values.tolist()
        MEIG = [s[0:-1] + '.T' for s in code if code_from < int(s[0:-1]) < code_to]
        logger.info(len(MEIG))
        if len(MEIG) > 1:
            return self._download_rate_to_df(MEIG)
        return None

    def download_rate(self):
        step = 1000
        for i in range(1000, 10000, step):
            logger.info("start download {} to {}".format(i, i + step))
            df = self.download_stockrate(i, i + step)
            if df is not None:
                filenm = self.filepath + "kabu_{}_{}.csv".format(i, i + step)
                logger.info("start output {}".format(filenm))
                df.to_csv(filenm)
            logger.info("finish {} to {}".format(i, i + step))

    def file_format(self):
        ret = pd.DataFrame()

        step = 1000
        for i in range(1000, 10000, step):
            in_filenm = self.filepath + "kabu_{}_{}.csv".format(i, i + step)
            logger.info("convert start input file = {}".format(in_filenm))

            df = pd.read_csv(in_filenm, index_col=0, header=[0, 1])
            df = df.stack(level=0)
            df = df.reset_index()
            df = df.set_axis(['Date', 'Symbol', 'AdjClose', 'Close', 'High', 'Low', 'Open', 'Volume'], axis='columns')
            df = df.set_index('Date')
            ret = pd.concat([ret, df])

        out_filenm = self.out_file()
        ret.to_csv(out_filenm)
        logger.info("convert_finish output file = {}".format(out_filenm))


if __name__ == '__main__':
    from logging import DEBUG

    logger.setLevel(DEBUG)
    man = YFinanceManager()
    man.download_rate_from_symbols(symbol.OvrEtf)

    from s3_data_manager import S3DataManager

    dm = S3DataManager(settings.config)
    dm.upload_dataframe(dataframe=man.df, key=settings.OVR_ETF_DATA)

    df = dm.download_datafile('ovr_etf.csv')
    print(df.head())
