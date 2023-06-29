import shutil
from os import path, listdir, rmdir, walk

import requests


def get_file_paths(folder_path):
    file_paths = []
    for root, dirs, files in walk(folder_path):
        for file in files:
            file_path = path.join(root, file)
            file_paths.append(file_path)
    return file_paths


def move_files_up_and_remove_folder(folder_path):
    move_to_path = None
    if folder_path:
        parent_path = path.dirname(folder_path)
        for file_name in listdir(folder_path):
            if path.exists(path.join(parent_path, file_name)):
                move_to_path = get_unique_filename(path.join(parent_path, file_name))
            else:
                move_to_path = path.join(parent_path, file_name)

            file_path = path.join(folder_path, file_name)
            shutil.move(file_path, move_to_path)

        rmdir(folder_path)
    # I wrote the code above with the assumption that move_to_path can't be None value
    return move_to_path


# def move_files_up_and_remove_folder(folder_paths):
#     out_file_paths = []
#     for folder_path in folder_paths:
#         out_file_paths.append(move_file_up_and_remove_folder(folder_path))
#     return out_file_paths


def get_unique_filename(file_path):
    base_dir = path.dirname(file_path)
    base_name, ext = path.splitext(path.basename(file_path))

    counter = 1
    while path.exists(file_path):
        new_name = f"{base_name}_{counter}{ext}"
        file_path = path.join(base_dir, new_name)
        counter += 1

    return file_path


def download_file(url, filename, file_path):
    file_path = path.join(file_path, filename)
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"File downloaded successfully: {file_path}")
    else:
        print(f"Failed to download file: {url}")
