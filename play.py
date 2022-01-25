import argparse
from threading import Thread
from hand_detector import detect_hands
from voice_detector import detect_voice


IMAGE_MODEL_PATH='trained_models/image'
IMAGE_MIN_CONFIDENCE=0.5
ROI_X=200
ROI_Y=200
ROI_WIDTH=600
ROI_HEIGHT=600

VOICE_MODEL_PATH='trained_models/voice'
VOICE_MIN_CONFIDENCE=0.5
VOICE_THRESHOLD = 0.015


def thread_wrapper(fn, **kwargs):

    def _wrapper():
        fn(**kwargs)

    return _wrapper


if __name__ == "__main__":

    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)

    parser.add_argument(
        "--image_model_path",
        type=str,
        default=IMAGE_MODEL_PATH,
        help="Path to folder with trained image model"
    )

    parser.add_argument(
        "--image_min_confidence",
        type=float,
        default=IMAGE_MIN_CONFIDENCE,
        help="Minimal level of confidence for action to be considered as valid"
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

    parser.add_argument(
        "--voice_model_path",
        type=str,
        default=VOICE_MODEL_PATH,
        help="Path to folder with trained voice model"
    )

    parser.add_argument(
        "--voice_min_confidence",
        type=float,
        default=VOICE_MIN_CONFIDENCE,
        help="Minimal level of confidence for action to be considered as valid"
    )

    parser.add_argument(
        "--voice_threshold",
        type=float,
        default=VOICE_THRESHOLD,
        help="Minimal level of voice activity"
    )


    args = parser.parse_args()

    detect_hands_wrapper = thread_wrapper(
      detect_hands,
      model_path=args.image_model_path,
      min_confidence=args.image_min_confidence,
      handle_action=True,
      roi_x=args.roi_x,
      roi_y=args.roi_y,
      roi_width=args.roi_width,
      roi_height=args.roi_height
    )
    Thread(target=detect_hands_wrapper).start()


    detect_voice_wrapper = thread_wrapper(
      detect_voice,
      voice_threshold=args.voice_threshold,
      model_path=args.voice_model_path,
      min_confidence=args.voice_min_confidence,
      handle_action=True
    )
    Thread(target=detect_voice_wrapper).start()

