from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.layers import Input
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Lambda
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import RMSprop

from learning.models.make_model_base import ModelMakerBase


class ModelMakerResnet(ModelMakerBase):
    def make_model(self, input_shape, output_shape):

        inputs = Input(input_shape)
        import tensorflow
        inputs = Lambda(lambda x: tensorflow.tile(x, [1, 1, 1, 3]))(inputs)
        inputs = Lambda(preprocess_input)(inputs)
        base_model = ResNet50(
            weights='imagenet', input_tensor=inputs, input_shape=None,
            include_top=False, pooling='avg'
        )

        model = Sequential([
            base_model,
            Dense(output_shape, activation="linear")
        ])

        base_model.trainable = False

        optimizer = RMSprop(0.001)

        model.compile(loss='mse',
                      optimizer=optimizer,
                      metrics=['mae', 'mse'])

        return model


