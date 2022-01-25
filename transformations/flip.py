import imgaug.augmenters as iaa


def get_flipped_images(image):
    orientations = ['ud', 'lr', None]
    
    return list(map(lambda orient: flip_image(image, orient), orientations))


def flip_image(image, orient=None):
    if orient == 'ud':
        flipper = iaa.Flipud()
    elif orient == 'lr':
        flipper = iaa.Fliplr()
    else:
        return image

    return flipper(images=[image])[0]
