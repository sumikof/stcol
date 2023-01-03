import numpy
import pandas as pd
import settings


def convert_lookback_dataset(dataset, look_back=1):
    dataX = []
    for i in range(look_back, len(dataset)):
        dataX.append(dataset[i - look_back:i])
    return numpy.array(dataX)


def create_train_and_test_dataset(dataset, out_dataset, train_size, look_back):
    i_dataset = dataset.values
    o_dataset = out_dataset.values
    if len(i_dataset) != len(o_dataset):
        raise RuntimeError(
            f'in out dataframe length not equal in {len(i_dataset)},out {len(o_dataset)}')
    train_data_size = int(len(dataset) * train_size)
    train, test = i_dataset[0:train_data_size, :], i_dataset[train_data_size:len(i_dataset), :]
    trainX = convert_lookback_dataset(train, look_back)
    testX = convert_lookback_dataset(test, look_back)
    trainY = o_dataset[look_back:train_data_size, :]
    testY = o_dataset[train_data_size + look_back:len(o_dataset), :]
    return trainX, trainY, testX, testY


def make_result_dataset(dataset, symbol: str, shift_list: list, columns: list):
    df = dataset[symbol]
    if len(shift_list) != len(columns):
        raise RuntimeError()
    result_set = pd.concat([df.shift(periods=-30), ], axis=1)
    result_set.columns = columns
    return result_set


def dataframe_0_1_scaler(dataframe):
    from sklearn.preprocessing import MinMaxScaler
    scaler = MinMaxScaler(feature_range=(0, 1))
    df = pd.DataFrame(scaler.fit_transform(dataframe), columns=dataframe.columns, index=dataframe.index)
    return df


def dataframe_reshape(dataframe, drop_columns=None, fill_na=None):
    dataframe = dataframe.pivot_table(
        values=[settings.ADJUST_CLOSE], index=['Date'], columns=['Symbol'], aggfunc='sum')
    dataframe.columns = dataframe.columns.droplevel(0)

    if drop_columns is not None and len(drop_columns) > 0:
        dataframe = dataframe.drop(drop_columns, axis=1)
    dataframe = dataframe.fillna(method='bfill')

    if fill_na is not None:
        dataframe = dataframe.fillna(fill_na)
    return dataframe
