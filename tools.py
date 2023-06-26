import os
import shutil

# Function to retrieve the absolute file paths in a folder and its subdirectories
import requests


def get_file_paths(folder_path):
    file_paths = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_paths.append(file_path)
    return file_paths


# This function effectively moves all files within the given folder
# up one level and then removes the empty folder.
def move_files_up_and_remove_folder(folder_path):
    if folder_path is None:
        return
    parent_path = os.path.dirname(folder_path)

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        shutil.move(file_path, parent_path)
    os.rmdir(folder_path)


def download_file(url, filename, file_path):
    file_path = os.path.join(file_path, filename)

    response = requests.get(url)
    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"File downloaded successfully: {file_path}")
    else:
        print(f"Failed to download file: {url}")
