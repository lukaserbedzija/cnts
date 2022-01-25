import argparse
import math
import pyaudio
import wave
import librosa
import numpy
import keras
import os
from controller.cs import handle_action


MODEL_PATH='trained_models/voice'
MIN_CONFIDENCE=0.5
VOICE_THRESHOLD = 0.015
HANDLE_ACTION=True

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 22050

NUM_MFCC=13
N_FTT=2048
HOP_LENGTH=512

TEMP_PATH = '.temp/'
TEMPRORARY_WAV = TEMP_PATH + 'temp.wav'
ACTION_WAV = TEMP_PATH + 'action.wav'
THRESHOLD_WAV = TEMP_PATH + 'threshold.wav'


CATEGORIES = ["DOWN", "GO", "LEFT", "RIGHT", "STOP", "UP"]


microphone = pyaudio.PyAudio()


def root_mean_square(data):
  return math.sqrt(sum([0 if numpy.isnan(x) else x**2 for x in data]) / len(data))


def has_voice_activity(file_path):
  global VOICE_THRESHOLD
  
  samples, _ = librosa.load(file_path, sr=RATE)

  return root_mean_square(samples) > VOICE_THRESHOLD


def save_wav_file(file_path, data):
  global microphone

  wf = wave.open(file_path, 'wb')
  wf.setnchannels(CHANNELS)
  wf.setsampwidth(microphone.get_sample_size(FORMAT))
  wf.setframerate(RATE)
  if type(data) is list:
    wf.writeframes(b''.join(data))
  else:
    wf.writeframes(data)
  wf.close()


def find_threshold():
  global microphone

  stream = microphone.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

  frames = []
  print('Finding threshold started.')
  for i in range(0, int(RATE / CHUNK * 5)):
    frames.append(stream.read(CHUNK))

  save_wav_file(THRESHOLD_WAV, frames)
  samples, _ = librosa.load(THRESHOLD_WAV, sr=RATE)
  threshold = root_mean_square(samples)

  stream.stop_stream()
  stream.close()

  return threshold


def transform(file_path):
    samples, sample_rate = librosa.load(file_path)
    samples = numpy.resize(samples, RATE)

    mfccs = librosa.feature.mfcc(samples, sample_rate, n_mfcc=NUM_MFCC, n_fft=N_FTT,
                                        hop_length=HOP_LENGTH)
    out_sample = numpy.array([mfccs.T.tolist()])
    out_sample = out_sample[..., numpy.newaxis]

    return out_sample


def detect_voice(**kwargs):
    global VOICE_THRESHOLD
    VOICE_THRESHOLD = kwargs['voice_threshold']

    if not os.path.isdir(TEMP_PATH):
      os.mkdir(TEMP_PATH)

    model = keras.models.load_model(kwargs['model_path'])

    stream = microphone.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    frames = []
    
    print('Voice activity detection started!')
    while True:
      data = stream.read(CHUNK)

      save_wav_file(TEMPRORARY_WAV, data)

      if not has_voice_activity(TEMPRORARY_WAV):
        continue

      print('Voice activity detected.')

      for _ in range(0, int(RATE / CHUNK)):
        frames.append(stream.read(CHUNK))

      save_wav_file(ACTION_WAV, frames)
      frames.clear()

      samples = transform(ACTION_WAV)
      prediction = model.predict(samples)
      confidence, action = prediction[0][numpy.argmax(prediction)], CATEGORIES[numpy.argmax(prediction)]
      print('Predicted: ' + action + ' with: ' + str(confidence * 100) + '% confidence level.')

      if confidence > kwargs['min_confidence'] and kwargs['handle_action']:
        handle_action(action)


if __name__ == '__main__':  
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)

    parser.add_argument(
        "--mode",
        type=str,
        default='detect_voice',
        help="Mode: 'detect_voice' or 'detect_threshold'. Default: 'detect_voice'"
    )

    parser.add_argument(
        "--voice_threshold",
        type=float,
        default=VOICE_THRESHOLD,
        help="Minimal level of voice activity"
    )

    parser.add_argument(
        "--model_path",
        type=str,
        default=MODEL_PATH,
        help="Path to folder with trained model"
    )

    parser.add_argument(
        "--min_confidence",
        type=float,
        default=MIN_CONFIDENCE,
        help="Minimal level of confidence for action to be considered as valid"
    )

    parser.add_argument(
        "--handle_action",
        type=bool,
        default=HANDLE_ACTION,
        help="Apply action to Counter Strike 1.6"
    )

    args = parser.parse_args()

    if args.mode == 'detect_voice':
        detect_voice(
          voice_threshold=args.voice_threshold,
          model_path=args.model_path,
          min_confidence=args.min_confidence,
          handle_action=args.handle_action
        )
    else:
        print('Threshold: ' + str(find_threshold()))
