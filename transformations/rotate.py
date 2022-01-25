import imgaug.augmenters as iaa


def get_rotated_images(image):
    angles = [0, 90, 180, 270, None, None, None, None, None, None]

    return list(map(lambda angle: rotate_image(image, angle), angles))


def rotate_image(image, angle=None):
    if angle is not None:
        rotator = iaa.Sequential([iaa.Rotate(angle)])
    else:
        rotator = iaa.Sequential([iaa.Rotate(rotate=(-60, 60))])

    return rotator(images=[image])[0]
