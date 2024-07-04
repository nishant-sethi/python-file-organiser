#!/usr/bin/env python3

import random
import os
import shutil
import logging
from pathlib import Path
from utils.helpers import get_file_path

logging.basicConfig(level=logging.INFO)

def is_directory_present(path='.'):
    """
    Check if a directory is present at the given path.

    Args:
        path (str): The path to check. Defaults to the current directory.

    Returns:
        bool: True if a directory is present, False otherwise.
    """
    for item in os.listdir(path):
        if os.path.isdir(get_file_path(path, item)):
            return True
    return False

def get_random_file(directory: Path) -> Path:
    """
    Get a random file from the given directory.

    Args:
        directory (str): The path to the directory.

    Returns:
        str: The path to a random file, or None if no files are present.
    """
    if not directory.is_dir():
        logging.error(f'{directory} is not a directory')
        return None
    
    files = [f for f in directory.iterdir() if get_file_path(directory, f).is_file()]
    if not files:
        return None
    return random.choice(files)

def create_random_folder(path='.'):
    """
    Create a random folder in the given directory.

    Args:
        path (str): The path to the directory. Defaults to the current directory.

    Returns:
        str: The path to the created folder.
    """
    random_folder_name = f'folder_{random.randint(1000, 9999)}'
    random_folder_path = get_file_path(path, random_folder_name)
    print(f'creating folder at: {random_folder_path}')
    os.mkdir(random_folder_path)
    return random_folder_path

def move_file_to_folder(filename, folder):
    """
    Move a file to a specified folder.

    Args:
        filename (str): The name of the file to move.
        folder (str): The path to the folder to move the file to.
    """
    print(f'Moving file {filename} to {folder}')
    shutil.move(filename, folder)
    
def create_folder_and_move_file(filename, path='.'):
    """
    Create a random folder in the given directory and move a file to it.

    Args:
        filename (str): The name of the file to move.
        path (str): The path to the directory. Defaults to the current directory.
    """
    random_folder = create_random_folder(path)
    logging.info(f'Folder created')
    logging.info('move file: {}'.format(filename))
    move_file_to_folder(get_file_path(path,filename), random_folder)
    logging.info(f'Moved file {filename} to {random_folder}')
