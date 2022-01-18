from logging import basicConfig
from logging import getLogger
from logging import DEBUG

import pandas as pd
import matplotlib.pyplot as plt

import s3_data_manager
import settings
import symbol
from learning.dataset import create_train_and_test_dataset

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


def dataframe_reshape(dataframe):
    dataframe = dataframe.pivot_table(
        values=[settings.ADJUST_CLOSE], index=['Date'], columns=['Symbol'], aggfunc='sum')
    dataframe.columns = dataframe.columns.droplevel(0)
    dataframe = dataframe.dropna(subset=dataframe.columns)
    return dataframe


def plot_dataframe(dataframe):
    plt.figure()
    #    dataframe.plot()
    plt.legend(loc='best')
    ax = dataframe.plot()
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


def make_model(input_shape):
    from tensorflow.keras.layers import LSTM
    from tensorflow.keras.layers import Dense
    from tensorflow.keras.layers import Input
    from tensorflow.keras.layers import TimeDistributed
    from tensorflow.keras.models import Model
    input = Input(input_shape)
    model = TimeDistributed(Dense(256))(input)
    model = TimeDistributed(Dense(64))(model)
    model = LSTM(32, return_sequences=False)(model)
    out = Dense(1)(model)
    model = Model(inputs=input, outputs=out)
    model.compile(loss='mean_squared_error', optimizer='adam')
    return model


def dl(train_size, look_back):
    dm = s3_data_manager.S3DataManager(settings.boto3_config)
    df = dm.download_datafile(key=settings.INDEX_DATA)
    df = dataframe_reshape(df)
    # df = dataframe_0_1_scaler(df)

    trainX, trainY, testX, testY = create_train_and_test_dataset(
        dataset=df,
        train_size=train_size,
        look_back=look_back)
    print(trainX)
    print(trainY)
#    model = make_model(input_shape=(look_back, testX.shape[2]))
#    model.summary()
#    model.fit(trainX, trainY, epochs=10, batch_size=1, verbose=2)


def main():
    dl(**settings.config)


if __name__ == '__main__':
    #basicConfig(level=DEBUG)
    # model = make_model(input_shape=(28, 3))
    # model.summary()
    main()
