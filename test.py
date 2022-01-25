import argparse
import keras
import preprocessors.preprocessor_factory as preprocessor_factory


INPUT_PATH = "datasets/test"
MODEL_PATH = "trained_model"

BATCH_SIZE = 128


def test(model_path, data, labels, **kwargs):
    model = keras.models.load_model(model_path)
    results = model.evaluate(data, labels, batch_size=kwargs['batch_size'])
    print("test loss, test acc:", results)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)

    parser.add_argument(
        "--input_path",
        type=str,
        default=INPUT_PATH,
        help="Path to folder with test dataset"
    )

    parser.add_argument(
        "--resource",
        type=str,
        help="Resource type of test dataset"
    )

    parser.add_argument(
        "--model_path",
        type=str,
        default=MODEL_PATH,
        help="Path to folder with trained model"
    )

    parser.add_argument(
        "--batch_size",
        type=int,
        default=BATCH_SIZE,
        help="Number of images processed in each iteration of training"
    )

    args = parser.parse_args()

    preprocessor = preprocessor_factory.create_preprocessor(args.resource)
    data, categories, labels = preprocessor(args.input_path)

    test(args.model_path, data, labels, batch_size=args.batch_size)

