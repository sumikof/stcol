from logging import basicConfig
from logging import getLogger
from logging import DEBUG

import pandas as pd
import matplotlib.pyplot as plt

import s3_data_manager
import settings
import symbol
from learning.dataset import create_train_and_test_dataset
from learning.dataset import make_result_dataset

logger = getLogger(__name__)


def calculate(meig):
    pass


def update_rate():
    pass


def dataframe_0_1_scaler(dataframe):
    from sklearn.preprocessing import MinMaxScaler
    scaler = MinMaxScaler(feature_range=(0, 1))
    df = pd.DataFrame(scaler.fit_transform(dataframe), columns=dataframe.columns, index=dataframe.index)
    return df


def dataframe_reshape(dataframe, drop_columns=[], fill_na=None):
    dataframe = dataframe.pivot_table(
        values=[settings.ADJUST_CLOSE], index=['Date'], columns=['Symbol'], aggfunc='sum')
    dataframe.columns = dataframe.columns.droplevel(0)

    if len(drop_columns) > 0:
        dataframe = dataframe.drop(drop_columns, axis=1)
    dataframe = dataframe.fillna(method='ffill')
    if fill_na is not None:
        dataframe = dataframe.fillna(fill_na)
    return dataframe


def plot_dataframe(dataframe):
    dataframe.plot()
    plt.show()


def download_yfinance(symbols):
    """
    :param symbols: download_yfinance(symbol.OvrIndex)
    :return:
    """
    from market import YFinanceManager
    man = YFinanceManager()
    man.download_rate_from_symbols(symbols)
    return man.df


def make_model(input_shape, output_shape):
    from tensorflow.keras.layers import LSTM
    from tensorflow.keras.layers import Dense
    from tensorflow.keras.layers import Input
    from tensorflow.keras.layers import Activation
    from tensorflow.keras.layers import TimeDistributed
    from tensorflow.keras.models import Model
    input = Input(input_shape)
    model = TimeDistributed(Dense(512))(input)
    model = LSTM(64, return_sequences=False)(model)
    model = Dense(32)(model)
    out = Dense(output_shape, activation="linear")(model)
    model = Model(inputs=input, outputs=out)
    model.compile(loss='mean_absolute_error', optimizer="sgd")
    # model.compile(loss='mean_squared_error', optimizer='adam')
    return model


def setup_input_output_data(predict_term):
    dm = s3_data_manager.S3DataManager(settings.boto3_config)
    index_dataset = dm.download_datafile(key=settings.INDEX_DATA)
    future_dataset = dm.download_datafile(key=settings.FUTURE_DATA)
    ovretf_dataset = dm.download_datafile(key=settings.OVR_ETF_DATA)
    bond_dataset = dm.download_datafile(key=settings.BOND_YIELDS_DATA)
    ex_dataset = dm.download_datafile(key=settings.EXCHANGE_RATE_DATA)

    df = pd.concat([index_dataset, future_dataset, ovretf_dataset, bond_dataset, ex_dataset])
    df = dataframe_reshape(df, fill_na=0)
    df = dataframe_0_1_scaler(df)

    result_set = make_result_dataset(df, '^N225', [-predict_term], ['n225-30'])
    input_dataset = df[result_set.isnull().sum(axis=1) == 0]
    output_dataset = result_set.dropna()
    input_dataset = input_dataset['2006-01-01':]
    output_dataset = output_dataset['2006-01-01':]

    return input_dataset, output_dataset


def fit_and_predict(input_dataset, output_dataset, train_size, look_back):
    trainX, trainY, testX, testY = create_train_and_test_dataset(input_dataset, output_dataset, train_size, look_back)

    model = make_model(input_shape=(look_back, testX.shape[2]), output_shape=1)
    model.summary()

    model.fit(trainX, trainY, epochs=10, batch_size=1, verbose=2)
    score = model.evaluate(trainX, trainY, batch_size=1, verbose=2)
    print(f'score is {score}')
    preds = model.predict(testX)

    result = pd.concat([pd.DataFrame(preds), pd.DataFrame(testY)], axis=1)
    result.columns = ['preds', 'test']
    plot_dataframe(result)
    print(result)


def main(train_size, look_back, predict_term):
    in_data, out_data = setup_input_output_data(predict_term)
    dset = pd.concat([in_data, out_data],axis=1)
    # dset = dset.dropna()
    print(dset.tail(200))
    df = dset.corr()
    print(df)
    # fit_and_predict(in_data, out_data, train_size, look_back)


if __name__ == '__main__':
    # basicConfig(level=DEBUG)
    main(**settings.config)
