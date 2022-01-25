import os
from keras.utils import np_utils
import numpy as np
import cv2 as cv


IMG_SIZE = 128


def create_preprocessor(input_dir):
    image_data = []
    labels = []
    categories = []

    for index, o in enumerate(os.listdir(input_dir)):
        if os.path.isdir(os.path.join(input_dir, o)):
            in_path = os.path.join(input_dir, o)
            categories.append(o)

            for img in os.listdir(in_path):
                try:
                    img_array = cv.imread(os.path.join(in_path, img))
                    img_resized = cv.resize(img_array, (IMG_SIZE, IMG_SIZE))

                    image_data.append(img_resized)
                    labels.append(index)
                except Exception as e:
                    print(e)

    processed_data = np.array(image_data).reshape((len(image_data), IMG_SIZE, IMG_SIZE, -1))
    image_labels = np_utils.to_categorical(y=labels, num_classes=len(categories))

    return processed_data, categories, image_labels
