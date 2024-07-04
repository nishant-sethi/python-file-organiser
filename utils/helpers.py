from pathlib import Path

def get_destination_folder(file_extension, file_extensions: dict) -> str:
    for extension in file_extensions:
        if file_extension in file_extensions[extension]:
            return extension
    return None

def get_file_extension(file_path: str) -> Path:
    return Path(file_path).suffix.lstrip('.').lower()

def get_file_path(*paths) -> Path:
    return Path(*paths).resolve()

def is_path_exists(path) -> bool:
    return Path(path).exists()