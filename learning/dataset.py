import numpy
import settings


def _create_dataset(dataset, look_back=1):
    dataX, dataY = [], []
    for i in range(len(dataset) - look_back - 1):
        xset = []
        for j in range(dataset.shape[1]):
            a = dataset[i:(i + look_back), j]
            xset.append(a)
        dataY.append(dataset[i + look_back, 0])
        xset = numpy.array(xset)
        dataX.append(xset.T)
    return numpy.array(dataX), numpy.array(dataY)


def create_train_and_test_dataset(dataset, train_size, look_back):
    dataset = dataset.values
    train_data_size = int(len(dataset) * train_size)
    test_size = len(dataset) - train_data_size
    train, test = dataset[0:train_data_size, :], dataset[train_data_size:len(dataset), :]
    trainX, trainY = _create_dataset(train, look_back)
    testX, testY = _create_dataset(test, look_back)
    return trainX, trainY, testX, testY
