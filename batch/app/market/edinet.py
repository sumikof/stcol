import pandas as pd
import settings
import os
from market.symbol import Stock


class Cols:
    pass


COLS = Cols()
COLS.CODE = '証券コード'

# ['日付', 'コード', '銘柄名', '市場・商品区分', '33業種コード', '33業種区分', '17業種コード', '17業種区分', '規模コード', '規模区分']
xlskeys = ['date', 'code', 'name', 'sijo', 'code33', 'kind33', 'code17', 'kind17', 'sizecode', 'sizekind']


def get_edinet_codes_df(file):
    """EDINETコードリストのデータフレーム取得"""
    # データフレーム生成
    df = pd.read_csv(
        file,
        encoding='cp932',
        dtype='str',
        skiprows=1,  # 最初の行をスキップ
        header=0,
    )
    return df


def edinet_kabu():
    df = get_edinet_codes_df(f'{settings.DATA_PATH}/EdinetcodeDlInfo.csv')
    # 上場企業だけを抽出
    df = df[df['上場区分'] == '上場']
    df = df.loc[:, ['ＥＤＩＮＥＴコード', COLS.CODE, '提出者名', '提出者業種', ]]
    # データフレームをリストに変換
    df = df.dropna(subset=[COLS.CODE])
    return [Stock(code=f'{row[1][0:4]}.T', name=row[2])
            for row in df[['証券コード', '提出者名']].itertuples() if row[1][0:4] != '0000']


def fund():
    df = get_edinet_codes_df('data/FundcodeDlInfo.csv')
    print(df.columns)
    # 上場企業だけを抽出
    df = df.dropna(subset=[COLS.CODE])
    return df[[COLS.CODE, 'ファンド名']]


def read_xls(file_name):
    df = pd.read_excel(os.path.join(settings.DATA_PATH, file_name))
    df.columns = xlskeys
    return [Stock(code=f'{row[1]}.T', name=row[2]) for row in df[['code', 'name']].itertuples()]


def kabu():
    return read_xls("data_j.xls")


if __name__ == "__main__":
    print(kabu())
