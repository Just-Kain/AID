import os

from file_utils import get_file_paths 


def _Start_work():
    dir_path = os.path.join("..", "657023")
    file_names = get_file_paths(folder_path=dir_path)
    
if __name__ == '__main__':
    _Start_work()
        