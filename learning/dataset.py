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
        raise RuntimeError()
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
