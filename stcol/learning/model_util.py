
def make_model_lstm(input_shape, output_shape):
    from tensorflow.keras.layers import LSTM
    from tensorflow.keras.layers import Dense
    from tensorflow.keras.layers import Input
    from tensorflow.keras.layers import Activation
    from tensorflow.keras.layers import TimeDistributed
    from tensorflow.keras.models import Model
    input = Input(input_shape)
#    model = TimeDistributed(Dense(128))(input)
    model = LSTM(512, return_sequences=True)(input)
    model = LSTM(256, return_sequences=True)(model)
    model = LSTM(128, return_sequences=False)(model)
    model = Dense(64)(model)
    model = Activation('relu')(model)
    model = Dense(32)(model)
    model = Activation('relu')(model)
    model = Dense(16)(model)

    out = Dense(output_shape, activation="linear")(model)
    model = Model(inputs=input, outputs=out)
    model.compile(loss='mean_absolute_error', optimizer="sgd")
    # model.compile(loss='mean_squared_error', optimizer='adam')
    return model


def make_model(input_shape, output_shape):
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Conv2D
    from tensorflow.keras.layers import Activation
    from tensorflow.keras.layers import MaxPool2D
    from tensorflow.keras.layers import Flatten
    from tensorflow.keras.layers import Dense
    from tensorflow.keras.layers import Dropout
    from tensorflow.keras.optimizers import RMSprop

    model = Sequential()

    model.add(Conv2D(32, 3, input_shape=input_shape))
    model.add(Activation('relu'))
    model.add(Conv2D(32, 3))
    model.add(Activation('relu'))
    model.add(MaxPool2D(pool_size=(2, 2)))

    model.add(Conv2D(64, 3))
    model.add(Activation('relu'))
    model.add(MaxPool2D(pool_size=(2, 2)))

    model.add(Flatten())
    model.add(Dense(1024))
    model.add(Activation('relu'))
    model.add(Dropout(1.0))

    model.add(Dense(output_shape))

    optimizer = RMSprop(0.001)

    model.compile(loss='mse',
                  optimizer=optimizer,
                  metrics=['mae', 'mse'])
    return model


