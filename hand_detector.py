import argparse
import keras
import cv2 as cv
import numpy as np
from transformations.extract import extract_max_hand_frame
from controller.cs import handle_action


IMG_SIZE = 128
MODEL_PATH='trained_models/image'
MIN_CONFIDENCE=0.5
HANDLE_ACTION=True
ROI_X=200
ROI_Y=200
ROI_WIDTH=600
ROI_HEIGHT=600


CATEGORIES = ["I", "II", "III", "IV", "B", "G", "LC", "RC", "R", "V"]


def preprocess_image(image):
    resized_image = cv.resize(image, (IMG_SIZE, IMG_SIZE))
    converted_image = cv.cvtColor(resized_image, cv.COLOR_GRAY2RGB)

    return np.array([converted_image])


def detect_hands(**kwargs):
    model = keras.models.load_model(kwargs['model_path'])

    video_capture = cv.VideoCapture(0)
    while True:
        _ , frame = video_capture.read()

        x, y, width, height = kwargs['roi_x'], kwargs['roi_y'], kwargs['roi_width'], kwargs['roi_height']
        roi = frame[x:width, y:height]
        cv.rectangle(frame, (x, y), (width, height), (0, 255, 0), 0)

        cv.imshow('frame', frame)

        max_frame = extract_max_hand_frame(roi)
        if max_frame is not None:
            cv.imshow("thresh", max_frame)

            processed_image = preprocess_image(max_frame)
            prediction = model.predict(processed_image)
            confidence, action = prediction[0][np.argmax(prediction)], CATEGORIES[np.argmax(prediction)]
            print('Predicted: ' + action + ' with: ' + str(confidence * 100) + '% confidence level.')

            if confidence > kwargs['min_confidence'] and kwargs['handle_action']:
              handle_action(action)

        if cv.waitKey(1) == 27:
          break


if __name__ == '__main__':
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)

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

    parser.add_argument(
        "--roi_x",
        type=int,
        default=ROI_X,
        help="X coordinate for Region Of Interest"
    )

    parser.add_argument(
        "--roi_y",
        type=int,
        default=ROI_Y,
        help="Y coordinate for Region Of Interest"
    )

    parser.add_argument(
        "--roi_width",
        type=int,
        default=ROI_WIDTH,
        help="Width for Region Of Interest"
    )

    parser.add_argument(
        "--roi_height",
        type=int,
        default=ROI_HEIGHT,
        help="Height for Region Of Interest"
    )

    args = parser.parse_args()

    detect_hands(
        model_path=args.model_path,
        min_confidence=args.min_confidence,
        roi_x=args.roi_x,
        roi_y=args.roi_y,
        roi_width=args.roi_width,
        roi_height=args.roi_height,
        handle_action=args.handle_action
    )