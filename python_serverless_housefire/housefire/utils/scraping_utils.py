import os
import uuid
import pandas as pd


def create_temp_dir(base_path: str) -> str:
    """
    Create a new directory with a random name in the temp directory

    param: base_path: the path to the base directory to create the new directory in

    returns: the full path to the new directory
    """
    dir_name = str(uuid.uuid4())
    new_dir_path = os.path.join(base_path, dir_name)
    os.mkdir(new_dir_path)
    return new_dir_path


def delete_temp_dir(temp_dir_path: str) -> None:
    """
    Delete a directory and all of its contents
    USE WITH CAUTION

    param: temp_dir_path: the path to the directory to delete
    """
    try:
        for filename in os.listdir(temp_dir_path):
            file_path = os.path.join(temp_dir_path, filename)
            os.remove(file_path)
        os.rmdir(temp_dir_path)
    except Exception as e:
        print(f"Error deleting directory at {temp_dir_path}: {e}")
