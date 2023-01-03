import matplotlib.pyplot as plt
import pandas as pd

import stcol.db.model
from stcol.learning.dataset import create_train_and_test_dataset
from stcol.learning.dataset import make_result_dataset
from stcol.learning.dataset import dataframe_reshape
from stcol.learning.dataset import dataframe_0_1_scaler
from stcol.learning.models.make_model_base import ModelMakerBase
from stcol.data_connector import s3_data_manager


def plot_dataframe(dataframe):
    dataframe.plot()
    plt.show()


def setup_input_output_data(predict_term):
    index_dataset = s3_data_manager.S3DataManager(model=stcol.db.model.IndexRate).get_daily_data()
    future_dataset = s3_data_manager.S3DataManager(model=stcol.db.model.FutureRate).get_daily_data()
    ovretf_dataset = s3_data_manager.S3DataManager(model=stcol.db.model.OvrEtfRate).get_daily_data()
    bond_dataset = s3_data_manager.S3DataManager(model=stcol.db.model.BondYieldsRate).get_daily_data()
    ex_dataset = s3_data_manager.S3DataManager(model=stcol.db.model.ExchangeRate).get_daily_data()

    df = pd.concat([index_dataset, future_dataset, ovretf_dataset, bond_dataset, ex_dataset])
    df = dataframe_reshape(df, fill_na=0)
    df = dataframe_0_1_scaler(df)

    result_set = make_result_dataset(df, '^N225', [-predict_term], ['n225-30'])
    input_dataset = df[result_set.isnull().sum(axis=1) == 0]
    output_dataset = result_set.dropna()
    input_dataset = input_dataset['2006-01-01':]
    output_dataset = output_dataset['2006-01-01':]

    return input_dataset, output_dataset


def fit_and_predict(
        input_dataset,
        output_dataset,
        train_size,
        look_back,
        epochs,
        batch_size,
        model_maker: ModelMakerBase):
    train_x, train_y, test_x, test_y = create_train_and_test_dataset(
        input_dataset, output_dataset, train_size=train_size, look_back=look_back)

    model = model_maker.make_model(input_shape=(test_x.shape[1], test_x.shape[2]), output_shape=1)
    model.summary()

    model.fit(train_x, train_y, epochs=epochs, batch_size=batch_size, verbose=2)
    model.save('model_dmp')
    score = model.evaluate(train_x, train_y, batch_size=batch_size, verbose=2)
    print(f'score is {score}')
    preds = model.predict(test_x)

    test_y = pd.DataFrame(test_y)
    real_y = pd.concat([test_y.shift(periods=15), ], axis=1)

    result = pd.concat([pd.DataFrame(preds), test_y, real_y], axis=1)
    result.columns = ['preds', 'test', '^N225']
    result = result[result['test'] > 0.000001]
    plot_dataframe(result)
    print(result)


def in_data_corr(in_data, out_data):
    dset = pd.concat([in_data, out_data], axis=1)
    df = dset.corr()
    in_data = in_data[df[df['n225-30'] > 0.8]['n225-30'].index.drop('n225-30')]
    return in_data


def main(train_size, look_back, predict_term, epochs, batch_size):
    in_data, out_data = setup_input_output_data(predict_term)
    in_data = in_data_corr(in_data, out_data)
    # in_data = in_data.rolling(3).mean().dropna()
    # out_data = out_data.rolling(3).mean().dropna()
    from stcol.learning.models import model_maker
    fit_and_predict(in_data,
                    out_data,
                    train_size,
                    look_back,
                    epochs,
                    batch_size,
                    model_maker.ModelMaker())
