import argparse
import os
import calendar
import cv2 as cv
import imgaug as ia
import time
import random
from transformations.rotate import get_rotated_images
from transformations.flip import get_flipped_images
from transformations.extract import extract_max_hand_frame
from transformations.crop import get_cropped_images
from utils.func import flat_map
from utils.os import list_all_folders, list_all_images_in


INPUT_PATH = 'HandDataset'
OUTPUT_PATH = 'generated'


def split_test_and_train_data(base_output_dir, images, test_split):

    test_images = random.sample(images.keys(), int(len(images) * test_split))
    for test_image in test_images:
        cv.imwrite(os.path.join(base_output_dir, 'test', test_image), images[test_image])
        images.pop(test_image)

    for filepath, image in images.items():
        cv.imwrite(os.path.join(base_output_dir, 'train', filepath), image)



def timestamp():
    gmt = time.gmtime()
    ts = calendar.timegm(gmt)

    return str(ts)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)

    parser.add_argument(
        "--input_path",
        type=str,
        default=INPUT_PATH,
        help="Path to folder with original dataset"
    )

    parser.add_argument(
        "--output_path",
        type=str,
        default=OUTPUT_PATH + '_' + timestamp(),
        help="Path to folder where transformed dataset will be saved"
    )

    parser.add_argument(
        "--test_split",
        type=float,
        default=0.1,
        help="Percentage of dataset to be used for test"
    )

    args = parser.parse_args()


    base_output_path = args.output_path
    input_path = args.input_path
    test_split = args.test_split

    os.mkdir(base_output_path)
    os.mkdir(os.path.join(base_output_path, 'train'))
    if test_split:
        os.mkdir(os.path.join(base_output_path, 'test'))

    images = {}

    for folder in list_all_folders(input_path):
        os.mkdir(os.path.join(base_output_path, 'train', folder))
        if test_split:
            os.mkdir(os.path.join(base_output_path, 'test', folder))

        counter = 0

        for image in list_all_images_in(os.path.join(input_path, folder)):
            open_cv_image = cv.imread(os.path.join(input_path, folder, image))

            rotated_images = get_rotated_images(open_cv_image)
            flipped_images = flat_map(lambda image: get_flipped_images(image), rotated_images)
            max_frames = list(map(lambda image: extract_max_hand_frame(image), flipped_images))
            cropped_images = flat_map(lambda image: get_cropped_images(image), max_frames)

            for img in cropped_images:
                counter = counter + 1
                images[folder + '/' + str(counter) + '.jpg'] = ia.imresize_single_image(img, (512, 512))
                
    
    split_test_and_train_data(base_output_path, images, test_split)
