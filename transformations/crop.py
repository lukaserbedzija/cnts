import imgaug.augmenters as iaa


def get_cropped_images(image):
    percentages = [0, 0.02, 0.06, 0.08, 0.12, 0.15]

    return list(map(lambda percent: crop_image(image, percent), percentages))


def crop_image(image, percent):
    cropper = iaa.Sequential([iaa.Crop(percent=percent)])

    return cropper(images=[image])[0]
