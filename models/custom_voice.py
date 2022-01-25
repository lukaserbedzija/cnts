from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, BatchNormalization


def create_model(num_of_labels, input_shape):
    model = Sequential()

    model.add(Conv2D(32, (3, 3), input_shape=input_shape))
    model.add(Activation('relu'))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2), padding="same"))
    model.add(Dropout(0.3))

    model.add(Conv2D(64, (3, 3)))
    model.add(Activation('relu'))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2), padding="same"))
    model.add(Dropout(0.3))

    model.add(Conv2D(128, (2, 2)))
    model.add(Activation('relu'))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2), padding="same"))
    model.add(Dropout(0.3))

    model.add(Conv2D(256, (1, 1)))
    model.add(Activation('relu'))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2), padding="same"))
    model.add(Dropout(0.3))

    model.add(Flatten())

    model.add(Dense(256))
    model.add(Activation('relu'))
    model.add(Dropout(0.3))

    model.add(Dense(128))
    model.add(Activation('relu'))
    model.add(Dropout(0.3))

    model.add(Dense(64))
    model.add(Activation('relu'))
    model.add(Dropout(0.3))

    model.add(Dense(num_of_labels))
    model.add(Activation('softmax'))

    return model
