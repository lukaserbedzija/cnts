import preprocessors.image as image
import preprocessors.sound as sound

def create_preprocessor(resource_type):
    create_preprocessor_methods = {
        'image': image.create_preprocessor,
        'sound': sound.create_preprocessor
    }

    if resource_type not in create_preprocessor_methods:
        print(resource_type + ' is not valid resource!')

        return None

    return create_preprocessor_methods[resource_type]

