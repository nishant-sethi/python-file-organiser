#!/usr/bin/env python3

"""
This module provides functionalities for managing and organizing files within directories. It includes features for creating folders, traversing directories, rearranging files based on certain criteria, and more. The main class, `FileManager`, offers methods to handle file management tasks efficiently.

Classes:
    FileManager: A class that provides methods for managing files and directories.

Functions:
    main: The entry point for executing the file management operations from the command line.

Usage:
    To use this script from the command line, you can pass the directory path to traverse and manage files using the `--dir` argument. Optionally, you can specify the `--rearrange` flag to enable rearranging files within the specified directory.

    Example:
    ```
    python folder_cleanup.py --dir "/path/to/directory" --rearrange
    ```

Dependencies:
    - os
    - shutil
    - argparse
    - pathlib.Path
    - file_util_helpers (create_random_folder, get_random_file, is_directory_present, move_file_to_folder)
    - image_file_extractor.ImageFeatureExtractor
"""

import logging
import os
import shutil
import argparse
from pathlib import Path
from utils.file_util_helpers import create_folder_and_move_file, get_random_file, is_directory_present, move_file_to_folder
from utils.helpers import get_destination_folder, get_file_extension, get_file_path, is_path_exists
from utils.image_file_extractor import ImageFeatureExtractor
import json

logging.basicConfig(level=logging.INFO)

class FileManager:

    image_feature_extractor = ImageFeatureExtractor()

    def __init__(self, file_extensions=None):
        if file_extensions is None:
            logging.error('File extensions not provided.')
            return
        self.file_extensions = file_extensions

    def rearrange_current_directory(self, current_directory: Path):
        """
        Rearranges the files in the current directory by moving them to the most similar directory.

        Args:
            current_directory (str): The path of the current directory.
            image_feature_extractor (ImageFeatureExtractor): An instance of the ImageFeatureExtractor class.

        Returns:
            None
        """
        if not is_path_exists(current_directory):
            logging.error(f'Directory {current_directory} does not exist.')
            return
        else:
            logging.info(f'Current directory: {current_directory}')
            files_in_dir = [f for f in current_directory.iterdir() if get_file_path(current_directory, f).is_file()
                ]
            logging.info(f'Files in directory: {files_in_dir}')

            # Iterate over each file in the current directory
            for _file in files_in_dir:
                logging.info(f'Processing file : {_file}')
                if _file.name.startswith('.DS_Store'):
                    if is_path_exists(get_file_path(current_directory, _file)):
                        logging.warning('removing .DS_Store file')
                        get_file_path(current_directory, _file).unlink()
                        continue

                # Process the file
                self.__process_file(current_directory, _file)
                print('\n')

    def __process_file(self, current_directory, _file):
        logging.info(f'Check if there are directories in the current directory: {
                     is_directory_present(current_directory)}')

        # Check if there are directories in the current directory
        if is_directory_present(current_directory):
            logging.info(f'Selected random file: {_file}')
            # Initialize similarity variables
            highest_similarity = 0
            most_similar_directory = None
            full_path_random_file = get_file_path(current_directory, _file)

            # Iterate over each directory in the current directory
            for item in current_directory.iterdir():
                dir_path = get_file_path(current_directory, item)
                if not dir_path.is_dir():
                    continue  # skip if it's not a directory

                # Pick a random file from the directory to compare
                random_file_in_dir = get_random_file(dir_path)
                if not random_file_in_dir or random_file_in_dir.name.startswith('.DS_Store'):
                    logging.warning(f'No file found in {
                                    dir_path} or it is a .DS_Store file, Skipping...')
                    continue  # skip if no file found or it's a .DS_Store file

                full_path_random_file_in_dir = get_file_path(
                    dir_path, random_file_in_dir)

                # Calculate similarity between the random file and the file in the directory
                similarity = FileManager.image_feature_extractor.get_similarity_score(
                    full_path_random_file, full_path_random_file_in_dir)
                logging.info(f'Comparing with file: {random_file_in_dir} in {
                             dir_path} with similarity: {similarity}')

                # Update the most similar directory if the similarity is higher and above a threshold,  and break if similarity is very high and current directory is the most similar directory
                if similarity > highest_similarity and similarity > 0.5:
                    highest_similarity = similarity
                    most_similar_directory = dir_path
                    if similarity > 0.7:
                        break

            # Move the random file to the most similar directory
            if most_similar_directory:
                move_file_to_folder(get_file_path(
                    current_directory, _file), most_similar_directory)
                logging.info(f'Moved file {_file} to {most_similar_directory}')
            # If no suitable directory found, create a new folder and move the file
            else:
                logging.info(
                    'No suitable directory found to move the file, creating a new folder...')
                create_folder_and_move_file(_file, current_directory)

        # If no directories found, create a new folder and move the file
        else:
            logging.info(
                'No directory found to move the file, creating a new folder...')
            create_folder_and_move_file(_file, current_directory)

    def rearrange_directory(self, dir_path):
        directories_to_process = []

        for dirpath, dirnames, filenames in os.walk(dir_path):
            for dirname in dirnames:
                directories_to_process.append(get_file_path(dirpath, dirname))

        for directory in directories_to_process:
            logging.info(f'Processing directory: {directory}')
            self.rearrange_current_directory(directory)
            logging.info(f'End of directory processing: {directory}')

    def traverse_directory(self, dir_path=Path.cwd()):
        logging.info('Traversing directory: {}'.format(dir_path))
        error_file_list = []
        for dirpath, dirnames, filenames in os.walk(dir_path):
            for file_name in filenames:
                filepath = get_file_path(dirpath, file_name)
                logging.info('Moving file: {}'.format(filepath))
                if self.__move_file(file_name, dir_path):
                    logging.info('File moved: {}'.format(file_name))
                else:
                    if not is_path_exists(filepath):
                        logging.error(
                            'Some error occured in moving file: {}'.format(file_name))
                        error_file_list.append(file_name)
        if len(error_file_list) > 0:
            logging.info('Error moving {} files'.format(len(error_file_list)))
            logging.info(error_file_list)
        else:
            logging.info('All files moved successfully')
        logging.info('End of directory traversal')
        print('\n')

    def create_folder(self, folders, dir_path=Path.cwd()):
        logging.info('Folder creating in directory:', dir_path)
        for folder in folders:
            path = get_file_path(dir_path, folder)
            if not is_path_exists(path):
                path.mkdir(parents=True, exist_ok=True)
                logging.info('Folder created: {}'.format(path))
            else:
                logging.info('Folder already exists: {}'.format(path))
        print('\n')

    def __move_file(self, file_name: str, root: str) -> bool:
        src = get_file_path(root, file_name)
        if not is_path_exists(src):
            logging.error('File does not exist: {}'.format(file_name))
            return None

        file_extension = get_file_extension(file_name)
        dest = get_destination_folder(file_extension, self.file_extensions)
        
        if not dest:
            return False
        final_path = get_file_path(root, dest, file_extension)
        
        if is_path_exists(final_path):
            logging.info('Directory already exists: {}'.format(final_path))
            
        else:
            logging.info(
                'Directory does not exist: {}, creating...'.format(final_path))
            final_path.mkdir(parents=True, exist_ok=True)
            logging.info('Directory created: {}'.format(final_path))

        final_dest = get_file_path(final_path, file_name)
        dest_path = shutil.move(src, final_dest)
        logging.info('File moved to dest: {}'.format(dest_path))
        return True

# Main function to execute the file management operations    
def main(file_extension, rearrange, traverse_path):
    file_manager = FileManager(file_extension)
    # Create folders for images and documents
    file_manager.create_folder(dict(file_extension).keys(), traverse_path)
    logging.info('Path traversing: {}'.format(traverse_path))
    file_manager.traverse_directory(traverse_path)
    if rearrange:
        # Rearrange the images directory
        # Note: Please ensure that the 'images' key is present in the config.json file when running this script. This limitation is currently being addressed.
        file_manager.rearrange_directory(get_file_path(traverse_path, 'images'))

if __name__ == "__main__":
    # Load file extensions from config.json
    try:
        file_extension = json.load(open('config.json', 'r')).get('FILE_EXTENSIONS')
    except Exception as e:
        logging.error(f"Error loading file extensions from config.json: {e}")
        file_extension = None
    
    # Parse command line arguments
    try:
        parser = argparse.ArgumentParser(
            description="File Manager and Image Feature Extractor")
        parser.add_argument("--dir", required=True, type=str,
                            help="Directory path to traverse and manage files")
        parser.add_argument("--rearrange", required=False, default=False,
                            type=bool, help="Directory path to traverse and manage files")

        args = parser.parse_args()
        dir_path = args.dir
        rearrange = args.rearrange
        traverse_path = Path(dir_path)
    except Exception as e:
        logging.error(f"Error parsing command line arguments: {e}")
        dir_path = None
        rearrange = False
        traverse_path = None
    
    # Create an instance of the FileManager class
    if file_extension is not None and dir_path is not None and traverse_path is not None:
        main(file_extension, rearrange, traverse_path)
    else:
        logging.error("Error: File extensions or directory path not provided.")
