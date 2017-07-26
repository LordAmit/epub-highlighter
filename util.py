import os


def check_if_path_exists(path: str):
    return os.path.exists(path)


def check_if_epub(file_path: str):
    file_base = os.path.splitext(file_path)[1]
    return file_base == ".epub"
