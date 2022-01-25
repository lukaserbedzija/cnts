import models.custom_hands as custom_hands
import models.custom_voice as custom_voice
import models.vgg_hands as vgg_hands


def create_model(model_type, num_of_labels, input_shape):
    create_model_methods = {
        'custom_hands': custom_hands.create_model,
        'custom_voice': custom_voice.create_model,
        'vgg_hands': vgg_hands.create_model
    }

    if model_type not in create_model_methods:
        print(model_type + ' is not valid model type!')

        return None

    return create_model_methods[model_type](num_of_labels, input_shape)
