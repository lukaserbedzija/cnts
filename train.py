import argparse
import preprocessors.preprocessor_factory as preprocessor_factory
import models.model_factory as model_factory

INPUT_PATH = "datasets/train"
MODEL_OUTPUT_PATH = "trained_model"

MODEL_TYPE = 'custom_hands'

BATCH_SIZE = 32
EPOCHS = 10
VALIDATION_SPLIT = 0.1


def find_resource(model_type):
    model_type_resources = {
        'custom_hands': 'image',
        'custom_voice': 'sound',
        'vgg_hands': 'image'
    }

    return model_type_resources[model_type]


def train_model(data, labels, model, model_output_path, **kwargs):
    model.compile(optimizer="adam",
                  loss="categorical_crossentropy",
                  metrics=["categorical_accuracy"])

    model.fit(data, labels, batch_size=kwargs['batch_size'], epochs=kwargs['epochs'], validation_split=kwargs['validation_split'])

    model.save(model_output_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)

    parser.add_argument(
        "--input_path",
        type=str,
        default=INPUT_PATH,
        help="Path to folder with training dataset"
    )

    parser.add_argument(
        "--model",
        type=str,
        default=MODEL_TYPE,
        help="Architecture of training model"
    )

    parser.add_argument(
        "--model_output_path",
        type=str,
        default=MODEL_OUTPUT_PATH,
        help="Path to folder where trained model will be saved"
    )

    parser.add_argument(
        "--batch_size",
        type=int,
        default=BATCH_SIZE,
        help="Number of images processed in each iteration of training"
    )

    parser.add_argument(
        "--epochs",
        type=int,
        default=EPOCHS,
        help="Number of epochs for training"
    )

    parser.add_argument(
        "--validation_split",
        type=float,
        default=VALIDATION_SPLIT,
        help="Percentage of training set to be used for validation"
    )

    args = parser.parse_args()


    resource = find_resource(args.model)

    preprocessor = preprocessor_factory.create_preprocessor(resource)
    data, categories, labels = preprocessor(args.input_path)

    model = model_factory.create_model(args.model, len(categories), (data.shape[1], data.shape[2], data.shape[3]))

    train_model(data, labels, model, args.model_output_path, batch_size=args.batch_size, epochs = args.epochs, validation_split = args.validation_split)