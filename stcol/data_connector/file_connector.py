import operator

import pandas as pd
import os
import settings
import re
from pathlib import Path
from stcol.data_connector.connector import Connector
from logging import getLogger

logger = getLogger(__name__)


class FileConnector(Connector):
    def __init__(self, model):
        super().__init__(model)

    operator_map = {
        "<": operator.lt,
        "<=": operator.le,
        ">": operator.gt,
        ">=": operator.ge,
    }

    @property
    def dirpath(self):
        return os.path.join(settings.DATA_PATH, self.model.__tablename__)

    @property
    def filename(self):
        return self.model.filename

    def getfilepath(self, date, count=0):
        if date is None:
            return self.searchfile()

        m = re.match(r"([<>=]*)([0-9]{8})", date)
        if m is None:
            raise RuntimeError(f"Not Dateformat => {date}")
        option = m.group(1)
        dateymd = m.group(2)
        logger.debug(f"compile date format option => [{option}], dateymd = {dateymd}")

        if option == "" or option == "=":
            return [os.path.join(self.dirpath, f'DAILY_{dateymd}_{self.filename}')]

        op = self.operator_map[option]
        return self.searchfile(dateymd, op, count)

    def searchfile(self, dateymd=None, op=None, count=0):
        def matchfile(filename, condition, op):
            m = re.match(r"[A-Z]+_([0-9]{8})_.+", filename)
            date = m.group(1)
            return op(date, condition)

        path = Path(self.dirpath)
        if dateymd is None:
            file_list = [file for file in path.glob(f'DAILY_*_{self.filename}')]
        else:
            file_list = [file for file in path.glob(f'DAILY_*_{self.filename}') if matchfile(file.name, dateymd, op)]

        file_list = sorted(file_list)
        if count < 1:
            return file_list
        return file_list[max(0, len(file_list) - count):]

    def get_daily_data(self, symbols=None, date=None, count=0):
        def readcsv(file_path):
            if symbols is not None and len(symbols) != 0:
                symbol_filter = [s.value for s in symbols]
                iter_csv = pd.read_csv(file_path,
                                       index_col=0, iterator=True, chunksize=5000)
                return pd.concat([chunk[chunk.Symbol.isin(symbol_filter)] for chunk in iter_csv])
            else:
                return pd.read_csv(file_path, index_col=0)

        file_path = self.getfilepath(date, count)
        logger.debug(f"read csv file filename => {file_path}")
        return pd.concat([readcsv(file) for file in file_path])

    def store_data(self, df, model):
        dirpath = self.dirpath
        os.makedirs(dirpath, exist_ok=True)

        uniq_indexs = sorted({_ for _ in df.index})
        for index_date in uniq_indexs:
            filepath = self.getfilepath(model, index_date)[0]
            df.loc[index_date].to_csv(filepath)
            logger.debug(f"stored csv file {filepath}")


if __name__ == '__main__':
    from logging import basicConfig, DEBUG

    basicConfig(level=DEBUG)
    con = FileConnector()
    dirpath = con.dirpath
    print(dirpath)

    filepath = con.getfilepath(model=settings.DOM_STOCK_DATA, date=None)
    print(filepath)
    filepath = con.getfilepath(model=settings.DOM_STOCK_DATA, date="20210804")
    print(filepath)
    filepath = con.getfilepath(model=settings.DOM_STOCK_DATA, date="=20210804")
    print(filepath)
    filepath = con.getfilepath(model=settings.DOM_STOCK_DATA, date=">20220521")
    print(filepath)
    for i in filepath:
        print(i.name)
