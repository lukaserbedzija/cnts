import os
import librosa
from keras.utils import np_utils
import numpy as np


RATE = 22050
NUM_MFCC=13
N_FFT=2048
HOP_LENGTH=512


def create_preprocessor(input_dir):
    sound_data = []
    labels = []
    categories = []

    for index, o in enumerate(os.listdir(input_dir)):
        if os.path.isdir(os.path.join(input_dir, o)):
            in_path = os.path.join(input_dir, o)
            categories.append(o)

            for file in os.listdir(in_path):
                try:
                    samples, sample_rate = librosa.load(os.path.join(in_path, file))

                    if len(samples) >= RATE:
                        samples = samples[:RATE]

                        mfccs = librosa.feature.mfcc(samples, sample_rate, n_mfcc=NUM_MFCC, n_fft=N_FFT,
                                                    hop_length=HOP_LENGTH)

                        sound_data.append(index)
                        labels.append(mfccs.T.tolist())
                except Exception as e:
                    print(e)

    processed_data = np.array(sound_data)
    processed_data = processed_data[..., np.newaxis]

    sound_labels = np_utils.to_categorical(y=labels, num_classes=len(categories))

    return processed_data, categories, sound_labels
