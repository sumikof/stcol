import pandas as pd


class Cols:
    pass


COLS = Cols()
COLS.CODE = '証券コード'


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


def kabu():
    df = get_edinet_codes_df('data/EdinetcodeDlInfo.csv')
    # 上場企業だけを抽出
    df = df[df['上場区分'] == '上場']

    # データフレームをリストに変換
    df = df.dropna(subset=[COLS.CODE])
    return df


def fund():
    df = get_edinet_codes_df('data/FundcodeDlInfo.csv')
    print(df.columns)
    # 上場企業だけを抽出
    df = df.dropna(subset=[COLS.CODE])
    return df[[COLS.CODE, 'ファンド名']]


if __name__ == '__main__':
    kabu()
