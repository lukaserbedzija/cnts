import os

def list_all_folders(input_path):
    for o in os.listdir(input_path):
        if os.path.isdir(os.path.join(input_path, o)):
            yield o


def list_all_images_in(folder):
    for o in os.listdir(folder):
        if o.lower().endswith(('.png', '.jpg', '.jpeg')):
            yield o
