from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras import layers, models


def create_model(num_of_labels, input_shape):
    base_model = VGG16(weights="imagenet", include_top=False, input_shape=input_shape)
    base_model.trainable = False

    flatten_layer = layers.Flatten()
    dense_layer_1 = layers.Dense(50, activation='relu')
    dense_layer_2 = layers.Dense(20, activation='relu')
    prediction_layer = layers.Dense(num_of_labels, activation='softmax')

    vgg_model = models.Sequential([
        base_model,
        flatten_layer,
        dense_layer_1,
        dense_layer_2,
        prediction_layer
    ])

    return vgg_model
